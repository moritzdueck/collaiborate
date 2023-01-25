## CollAIborate

### Environment Setup

```
conda create -n collaiborate python=3.9.7
conda activate collaiborate
pip install -r requirements.txt
```

If you want to start jupyter from within this conda env, run `conda install nb_conda_kernels` so that conda kernels are automatically detected.

### Train the CNN with the provided script
```
python collaiborate/train_script.py -t run1 \
--icons "airplane,apple,wine bottle,car,mouth,pineapple,umbrella,pear,moustache,smiley face,train,mosquito,bee,dragon,piano" \
--epochs 30 \
--learning_rate 0.001 \
--batch_size 64
```