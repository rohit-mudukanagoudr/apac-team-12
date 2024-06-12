#Add Azure OpenAI package
from openai import AzureOpenAI

AZURE_OAI_ENDPOINT= "https://testazureopenaione.openai.azure.com/"
AZURE_OAI_KEY= "0073dab2b2c04aac9bac7438547b25ce"
AZURE_OAI_DEPLOYMENT= "namma_gpt_4o_model"

def main():
    try:
        
        azure_oai_endpoint = AZURE_OAI_ENDPOINT
        azure_oai_key = AZURE_OAI_KEY
        azure_oai_deployment = AZURE_OAI_DEPLOYMENT

        #Initialize the Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint = azure_oai_endpoint,
            api_key = azure_oai_key,
            api_version = "2024-02-01"
        )

        #Create a system message
        system_message = """You are an helpful assistant and are well versed in generating SQL queries from questions asked by the user.\
        There are two tasks that you need to handle:
        1)Postgres SQL tables, with their properties:\
clients (
  client_id int NOT NULL,
  name varchar(50) NOT NULL,
  address varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state char(2) NOT NULL,
  phone varchar(50) DEFAULT NULL,
  PRIMARY KEY (client_id)
) ;

payment_methods (
  payment_method_id int NOT NULL,
  name varchar(50) NOT NULL,
  PRIMARY KEY (payment_method_id)
) ;
products (
  product_id int NOT NULL,
  name varchar(50) NOT NULL,
  quantity_in_stock int NOT NULL,
  unit_price decimal(4,2) NOT NULL,
  PRIMARY KEY (product_id)
)  ;
employees (
  employee_id int NOT NULL,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  job_title varchar(50) NOT NULL,
  salary int NOT NULL,
  reports_to int DEFAULT NULL,
  office_id int NOT NULL,
  PRIMARY KEY (employee_id),
) ;
offices (
  office_id int NOT NULL,
  address varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) NOT NULL,
  PRIMARY KEY (office_id)
) ;
order_item_notes (
  note_id INT NOT NULL,
  order_Id INT NOT NULL,
  product_id INT NOT NULL,
  note VARCHAR(255) NOT NULL,
  PRIMARY KEY (note_id));
invoices (
  invoice_id int NOT NULL,
  number varchar(50) NOT NULL,
  client_id int NOT NULL,
  invoice_total decimal(9,2) NOT NULL,
  payment_total decimal(9,2) NOT NULL DEFAULT 0.00,
  invoice_date date NOT NULL,
  due_date date NOT NULL,
  payment_date date DEFAULT NULL,
  PRIMARY KEY (invoice_id)
  ) ;
payments (
  payment_id int NOT NULL,
  client_id int NOT NULL,
  invoice_id int NOT NULL,
  date date NOT NULL,
  amount decimal(9,2) NOT NULL,
  payment_method tinyint NOT NULL,
  PRIMARY KEY (payment_id)
);
shippers (
  shipper_id smallint NOT NULL,
  name varchar(50) NOT NULL,
  PRIMARY KEY (shipper_id)
)  ;

customers (
  customer_id int NOT NULL,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  birth_date date DEFAULT NULL,
  phone varchar(50) DEFAULT NULL,
  address varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state char(2) NOT NULL,
  points int NOT NULL DEFAULT 0,
  PRIMARY KEY (customer_id)
)  ;

order_items (
  order_id int NOT NULL,
  product_id int NOT NULL,
  quantity int NOT NULL,
  unit_price decimal(4,2) NOT NULL,
  PRIMARY KEY (order_id,product_id)
  )  ;
order_statuses (
  order_status_id tinyint NOT NULL,
  name varchar(50) NOT NULL,
  PRIMARY KEY (order_status_id)
) ;
orders (
  order_id int NOT NULL,
  customer_id int NOT NULL,
  order_date date NOT NULL,
  status tinyint NOT NULL DEFAULT 1,
  comments varchar(2000) DEFAULT NULL,
  shipped_date date DEFAULT NULL,
  shipper_id smallint DEFAULT NULL,
  PRIMARY KEY (order_id)
  )  ;
transactions (
  payment_id int NOT NULL,
  client_id int NOT NULL,
  invoice_id int NOT NULL,
  date date NOT NULL,
  amount decimal(9,2) NOT NULL,
  payment_method tinyint NOT NULL,
  PRIMARY KEY (payment_id)
  )  ;
            Respond with "More information needed, try elaborating your question or specify the metrics you are looking for" \
            if unable to find the requested information\
        2)Depending on the type of data being retrieved check whether it can be represented visually:
         IF YES: Then suggest which graph to plot and assign the (x,y) co-ordinates according to the data(INCLUDE AGGREGATED DATA IF APPLICABLE)
         IF NO: Then respond saying "Can't be represented visually"

        DON'T INCLUDE ANY ADDITIONAL INFORMATION APART FROM SQL AND GRAPH
        """

        #Initialize messages array
        messages_array = [{"role":"system","content":system_message}]

        while True:
            #Get input text
            input_text = input("Enter the prompt( or type 'quit' to exit):")
            if input_text.lower()== 'quit':
                break
            if len(input_text)==0:
                print("What do you want to know about?")
                continue

            print("\n Sending request to Azure OpenAI endpoint..\n\n")

            #Send request to Azure OpenAI model
            messages_array.append({"role":"user","content":input_text})

            response = client.chat.completions.create(
                model = azure_oai_deployment,
                temperature = 0.7,
                max_tokens = 400,
                messages = messages_array
            )

            generated_text = response.choices[0].message.content

            #Add generated text to message-array
            messages_array.append({"role":"system","content":generated_text})

            print("Response: "+ generated_text + "\n")

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()