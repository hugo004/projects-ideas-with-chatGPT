
import os
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, load_index_from_storage, LLMPredictor, PromptHelper, ServiceContext, StorageContext, download_loader
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv('../../environments/.env')
os.environ['OPENAI_API_KEY'] = os.environ.get('OPEN_API_KEY')


max_input_size = 4096
num_outputs = 2000
max_chunk_overlap = 20
chunk_size_limit = 600

data_path = '../../data/pdf_training_sample1.pdf'


max_input_size = 4096
num_outputs = 2000
max_chunk_overlap = 20
chunk_size_limit = 600

prompt_helper = PromptHelper(max_input_size=max_input_size,
                             num_output=num_outputs,
                             max_chunk_overlap=max_chunk_overlap,
                             chunk_size_limit=chunk_size_limit
                             )

# open AI params
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5,
                                            model_name='gpt-3.5-turbo',
                                            max_tokens=num_outputs))

# load data from text files
# documents = SimpleDirectoryReader(data_path).load_data()

# load data from pdfs
PDFReader = download_loader("PDFReader")
pdf_loader = PDFReader()
documents = pdf_loader.load_data(file=data_path)

service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, prompt_helper=prompt_helper)
storage_context = StorageContext.from_defaults()

vector_index = GPTVectorStoreIndex.from_documents(documents=documents,
                                                  service_context=service_context,
                                                  storage_context=storage_context)
# save data to disk
vector_index.storage_context.persist(persist_dir='./storage')


if __name__ == '__main__':
    # load vector index from disk
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    vector_index = load_index_from_storage(storage_context=storage_context)

    query_engine = vector_index.as_query_engine()
    while True:
        query = input('What do you want to ask?\n')
        response = query_engine.query(query)
        print(response)
        print()
