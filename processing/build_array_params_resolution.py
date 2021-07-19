import json

with open('bboxes.json') as bbox:
    bboxes = json.load(bbox)

# Write the required params for each job into a file in the format:
# job_id shapefile_name(no extension) utm_zone north/south
with open('resolution_array_params.txt', 'w') as f:
    for i, (key, value) in enumerate(bboxes.items(), start=1):
        f.write('{} {} {} {}\n'.format(str(i).zfill(4), key[:-4], value['utm_zone'][0], value['utm_zone'][1]))
