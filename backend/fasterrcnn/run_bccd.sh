img_v=3
for s in val test train
do
    rm pvqa_data/images/${s}${img_v}.csv
    CUDA_VISIBLE_DEVICES=$1 python generate_tsv.py --net res101 --dataset bccd --load_dir . --image_dir data/pvqa/images/${s} --out data/pvqa/images/${s}${img_v}.csv --cuda --classes_dir data/bccd/
done