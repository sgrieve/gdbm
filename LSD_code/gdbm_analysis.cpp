//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//
// Copyright (C) 2016-2021 Simon M. Mudd & Stuart W.D. Grieve
//
// Developer can be contacted by s.grieve _at_ qmul.ac.uk
//
// This program is free software;
// you can redistribute it and/or modify it under the terms of the
// GNU General Public License as published by the Free Software Foundation;
// either version 3 of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY;
// without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU General Public License for more details.
//
// You should have received a copy of the
// GNU General Public License along with this program;
// if not, write to:
// Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor,
// Boston, MA 02110-1301
// USA
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <sys/time.h>
#include <fstream>
#include "../LSDStatsTools.hpp"
#include "../LSDChiNetwork.hpp"
#include "../LSDRaster.hpp"
#include "../LSDRasterInfo.hpp"
#include "../LSDIndexRaster.hpp"
#include "../LSDFlowInfo.hpp"
#include "../LSDJunctionNetwork.hpp"
#include "../LSDIndexChannelTree.hpp"
#include "../LSDBasin.hpp"
#include "../LSDChiTools.hpp"
#include "../LSDSpatialCSVReader.hpp"
#include "../LSDShapeTools.hpp"

int main (int nNumberofArgs,char *argv[])
{

  //Test for correct input arguments
  if (nNumberofArgs!=8)
  {
    cout << "Incorrect number of arguments - please refer to processing/runner.sh" << endl;
    cout << "to see how the interface to this code works." << endl;

    exit(EXIT_SUCCESS);
  }

  // Basic DEM preprocessing
  float min_slope_for_fill = 0.0001;

  // load our input args from the runner.sh script
  string DATA_DIR = argv[1];
  string DEM_ID = argv[2];
  string OUT_DIR = argv[3];
  string OUT_ID = argv[4];
  int threshold_contributing_pixels = atoi(argv[5]);
  int minimum_basin_size_pixels = atoi(argv[6]);
  int maximum_basin_size_pixels = atoi(argv[7]);

  string raster_ext = "bil";

  //set boundary conditions
  vector<string> boundary_conditions(4, "No Flux");

  cout << "Read filename is: " <<  DATA_DIR + DEM_ID << endl;
  cout << "Write filename is: " << OUT_DIR + OUT_ID << endl;

  // check to see if the raster exists
  LSDRasterInfo RI((DATA_DIR+DEM_ID), raster_ext);

  // Chi analysis values. These are not used in this analysis and can be ignored.
  float A_0 = 1;
  float movern = 0.5;
  int n_iterations = 20;
  int minimum_segment_length = 10;
  int n_nodes_to_visit = 10;
  float sigma = 20;
  int target_nodes = 80;
  int skip = 2;
  float thresh_area_for_chi = 0;

  // load the  DEM
  LSDRaster topography_raster((DATA_DIR+DEM_ID), raster_ext);

  cout << "Got the dem: " <<  DATA_DIR+DEM_ID << endl;

  map<string,string> GRS = topography_raster.get_GeoReferencingStrings();

  cout << "Let me fill that raster for you, the min slope is: "
       << min_slope_for_fill << endl;

  LSDRaster filled_topography = topography_raster.fill(min_slope_for_fill);


  // Now we do the diff between the filled and unfilled DEM
  Array2D<float> diff(filled_topography.get_NRows(), filled_topography.get_NCols(),filled_topography.get_NoDataValue());

  for (int i=0; i < filled_topography.get_NRows(); ++i){
    for (int j=0; j < filled_topography.get_NCols(); ++j){
      float diff_val = filled_topography.get_data_element(i,j) - topography_raster.get_data_element(i,j);

      if (diff_val > 0.0){
        diff[i][j] = diff_val;
      }
    }
  }

  vector<float> flat_diff = Flatten_Without_Nodata(diff, topography_raster.get_NoDataValue());

  vector<size_t> index_map;
  vector<float> data_sorted;
  matlab_float_sort(flat_diff, data_sorted, index_map);

  float diff_pc = get_percentile(data_sorted, 98.0);  // >2 standard devs of the mean

  string deltas_pc_name = OUT_DIR + OUT_ID + "_pit_id.csv";

  ofstream WritePitData;
  WritePitData.open(deltas_pc_name.c_str());

  for (int i=0; i < filled_topography.get_NRows(); ++i){
    for (int j=0; j < filled_topography.get_NCols(); ++j){

      if (diff[i][j] > diff_pc){
        WritePitData << i << "," << j << endl;

      }

    }
  }

  WritePitData.close();

  // End of the diffing between the 2 DEMs

  cout << "\t Flow routing..." << endl;
  // get a flow info object
  LSDFlowInfo FlowInfo(boundary_conditions,filled_topography);

  // calculate the flow accumulation
  cout << "\t Calculating flow accumulation (in pixels)..." << endl;
  LSDIndexRaster FlowAcc = FlowInfo.write_NContributingNodes_to_LSDIndexRaster();

  cout << "\t Converting to flow area..." << endl;
  LSDRaster DrainageArea = FlowInfo.write_DrainageArea_to_LSDRaster();

  // calcualte the distance from outlet
  cout << "\t Calculating flow distance..." << endl;
  LSDRaster DistanceFromOutlet = FlowInfo.distance_from_outlet();

  // load the sources
  vector<int> sources;

  cout << "Getting sources from a threshold of "<< threshold_contributing_pixels << " pixels." <<endl;
  sources = FlowInfo.get_sources_index_threshold(FlowAcc, threshold_contributing_pixels);

  cout << "The number of sources is: " << sources.size() << endl;

  // now get the junction network
  LSDJunctionNetwork JunctionNetwork(sources, FlowInfo);

  // need to get base-level nodes , otherwise these catchments will be missed!
  vector< int > BaseLevelJunctions;

  // remove basins drainage from edge
  cout << "I am going to look for basins in a contributing pixel window that are not influended by nodata." << endl;
  cout << "I am also going to remove any nested basins." << endl;
  BaseLevelJunctions = JunctionNetwork.Prune_Junctions_By_Contributing_Pixel_Window_Remove_Nested_And_Nodata(FlowInfo, filled_topography, FlowAcc,
                                            minimum_basin_size_pixels,maximum_basin_size_pixels);

  // Correct number of base level junctions
  int N_BaseLevelJuncs = BaseLevelJunctions.size();
  cout << "The number of basins I will analyse is: " << N_BaseLevelJuncs << endl;
  if (N_BaseLevelJuncs == 0)
  {
    cout << "I am stopping here since I don't have any basins to analyse." << endl;
    exit(EXIT_FAILURE);
  }

  // using the chi tools for their efficient channel processing, not actually calculating chi
  LSDChiTools ChiTool(FlowInfo);

  LSDRaster chi_coordinate;

  chi_coordinate = FlowInfo.get_upslope_chi_from_all_baselevel_nodes(movern,A_0,thresh_area_for_chi);

  // now source and outlet nodes for segmentation and other operations.
  vector<int> source_nodes;
  vector<int> outlet_nodes;
  vector<int> baselevel_node_of_each_basin;

  JunctionNetwork.get_overlapping_channels_to_downstream_outlets(FlowInfo, BaseLevelJunctions, DistanceFromOutlet,
                                source_nodes,outlet_nodes,baselevel_node_of_each_basin,n_nodes_to_visit);

  ChiTool.chi_map_automator(FlowInfo, source_nodes, outlet_nodes, baselevel_node_of_each_basin,
                          filled_topography, DistanceFromOutlet,
                          DrainageArea, chi_coordinate, target_nodes,
                          n_iterations, skip, minimum_segment_length, sigma);

  string csv_full_fname = OUT_DIR+OUT_ID+"_RawBasins.csv";
  cout << "Let me print all the data for you into a csv file called " << csv_full_fname << endl;
  ChiTool.print_gdbm_data_easting_northing(FlowInfo, JunctionNetwork, csv_full_fname);
  cout << "That is your file printed!" << endl;

}
