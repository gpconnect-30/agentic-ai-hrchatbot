import config, shutil
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def load_documents():
    files = []
    if Path(config.DATA_PATH).exists():
        #print(f"Found Data Directory", config.DATA_PATH)
        for items in Path(config.DATA_PATH).iterdir():
            #print(items.resolve())
            if items.resolve().suffix in config.SUPPORTED_EXTENSIONS:
                #print(f"Success! {items.resolve().suffix} is Supported format")
                files.append(items.resolve())
            else:
                print(f"Error: {items.resolve().suffix} is not a supported format")
        return files
    else:
        print("Path Directory not Found")

def extract_documents(files):
    document =[]
    for f in files:
        if f.suffix == ".txt":
            loader = TextLoader(f)
            document.extend(loader.load())
        else:
            print(f"{f.suffix} is not a txt format")
    return document

def split_documents(extract_documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = text_splitter.split_documents(extract_documents)
    return split_docs


def save_to_chroma(chunks, documents):
    embeds = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
    # Removing old database
    file_path = Path(config.VECTORSTORE_PATH)
    shutil.rmtree(file_path)

    vector_store = Chroma.from_documents(
        embedding=embeds,
        documents=(chunks),
        persist_directory=config.VECTORSTORE_PATH        
        )
    
    print("=====================================")
    print("Vector Database Created Successfully")
    print("=====================================")
    print("Documents: ", len(documents))
    print("Chunks: ", len(chunks))
    

def main():
    files = load_documents()
    documents = extract_documents(files)
    chunks = split_documents(documents)
    save_to_chroma(chunks, documents)

if __name__ == "__main__":
    main()