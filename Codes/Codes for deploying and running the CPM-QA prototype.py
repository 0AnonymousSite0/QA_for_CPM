#All commands are entered at the Anaconda Prompt terminal.

conda --version

#Create a virtual environment for Python running
conda create -n langchain_chatchat python=3.10.12  #langchain_chatchat is the name of virtual environment you have set up.

#Activate the virtual environment
conda activate langchain_chatchat

#Install PyTorch
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

#Pull from the repository
git clone https://github.com/chatchat-space/Langchain-Chatchat.git

cd Langchain-Chatchat
pip install -r requirements.txt
pip install -r requirements_api.txt
pip install -r requirements_webui.txt

#Download models you need
git lfs install
git clone https://huggingface.co/THUDM/chatglm3-6b
git clone https://huggingface.co/BAAI/bge-large-zh

python copy_config_example.py
python init_database.py --recreate-vs

#Replace the webui.py file, webui_pages folder, img folder, and knowledge_base folder within the Langchain-Chatchat directory
#Run the prototype
python startup.py -a