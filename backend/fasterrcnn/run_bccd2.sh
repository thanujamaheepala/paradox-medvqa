img_v=3
for s in val
do
    rm data/pvqa/${s}${img_v}.csv
    CUDA_VISIBLE_DEVICES=$1 python generate_tsv.py --net res101 --dataset bccd --load_dir . --image_dir data/pvqa/${s} --out data/pvqa/${s}${img_v}.csv
done