.DEFAULT_GOAL := run
INPUT=inputs
OUTPUT=outputs
IN_RESIZE=in_resize
OUT_RESIZE=out_resize
COMB=combined
EPOCHS=300
TRAIN=lesions_train
TEST=lesions_test
ROOT=output/pix2pix

# Removes old data
clean:
	rm -rf $(ROOT)/$(INPUT) $(ROOT)/$(OUTPUT) $(ROOT)/$(IN_RESIZE) $(ROOT)/$(OUT_RESIZE) $(ROOT)/$(COMB) $(ROOT)/$(TRAIN) $(ROOT)/$(TEST)
# Converts all dicom images in the data dir to pngs
convert:
	python3 tools/mri_to_png.py
# Runs resizing tool to make all images same size
resize:
	python3 tools/process.py --input_dir $(ROOT)/$(INPUT) --operation resize --output_dir $(ROOT)/$(IN_RESIZE)
	python3 tools/process.py --input_dir $(ROOT)/$(OUTPUT) --operation resize --output_dir $(ROOT)/$(OUT_RESIZE)
# Combines input and output images side by side for pix2pix
combine:
	python3 tools/process.py --input_dir $(ROOT)/$(IN_RESIZE) --b_dir $(ROOT)/$(OUT_RESIZE) --operation combine --output_dir $(ROOT)/$(COMB)
# Splits the data into training and testing
split:
	python3 tools/split.py --dir $(ROOT)/$(COMB)
# Runs the pix2pix model on the training data utilizing GPU Tensorflow
train:
	python3 pix2pix.py --mode train --output_dir $(ROOT)/$(TRAIN) --max_epochs $(EPOCHS) --input_dir $(ROOT)/$(COMB)/train --which_direction AtoB
# Runs the trained model on testing data
test:
	python3 pix2pix.py --mode test --output_dir $(ROOT)/$(TEST) --input_dir $(ROOT)/$(COMB)/val --checkpoint $(ROOT)/$(TRAIN)
# Runs pre-processing pipeline
run: clean convert resize combine split