# make with make -f gdbm_analysis.make

CC=g++
CFLAGS=-c -Wall -O3
OFLAGS = -Wall -O3
LDFLAGS= -Wall
SOURCES=gdbm_analysis.cpp \
             ../LSDMostLikelyPartitionsFinder.cpp \
             ../LSDIndexRaster.cpp \
             ../LSDRaster.cpp \
             ../LSDRasterInfo.cpp \
             ../LSDFlowInfo.cpp \
             ../LSDJunctionNetwork.cpp \
             ../LSDIndexChannel.cpp \
             ../LSDChannel.cpp \
             ../LSDIndexChannelTree.cpp \
             ../LSDStatsTools.cpp \
             ../LSDShapeTools.cpp \
             ../LSDChiNetwork.cpp \
             ../LSDBasin.cpp \
             ../LSDParticle.cpp \
             ../LSDChiTools.cpp \
             ../LSDSpatialCSVReader.cpp \
             ../LSDCRNParameters.cpp \
             ../LSDRasterMaker.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=gdbm_analysis.exe

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f ../*.o *.o *.out *.exe
