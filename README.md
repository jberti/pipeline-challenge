# Technical Challenge Solution

## Initial Notes

For this work, I opted to use meltano, as it seemed interesting to me because it runs on Python, has good documentation and is relatively simple to use. I had never worked with this technology before, which turned out to be quite a challenge.

I'd like to point out that when using Airflow, I wasn't able to use the option of integrating it with Meltano as a de facto orchestrator. This was due to an error when it was installed.
![Erro ao tentar instalar airflow como orchestrador](https://i.imgur.com/fdTAQ3Q.png)

Because of this, at DAG I ended up making the calls to Meltano via BashOperator, which is, according to the Meltano documentation, a valid option.

But I believe that this ended up limiting my configuration options, where, for example, I was unable to meet the requirement to allow a start date to be provided for reading the data to be integrated. Perhaps I was also limited in fulfilling the requirement to create a directory with the current day's date in the path of the files to be saved.


Translated with DeepL.com (free version) 

## Technologies

* **Programming Language:** Python
* **Framework:** Meltano, Airflow
* **Database:** PostgreSQL
* **Other Technologies:** Docker

## Environment

* OS running the project was Ubunu 22.04.5 LTS
* Must configure Airflow to point to the project dags folder
* Must start the database, running the docker compose up command. Current port is 5435

## Running the pipeline
After setting up the enviroment, you should access the airflow web interface and search for the following DAGS 
- Extraction data from file system to Postgres
- Extraction data to file system

Running DAG "Extraction data from file system to Postgres" will trigger DAG "Extraction data to file system"

## Results

### Of the requirements defined, the results were:
  
#### Met
- You must use the tools described above to complete the challenge.
- All tasks should be idempotent, you should be able to run the pipeline everyday and, in this case where the data is static, the output shold be the same.
- Step 2 depends on both tasks of step 1, so you should not be able to run step 2 for a day if the tasks from step 1 did not succeed.
- You should extract all the tables from the source database, it does not matter that you will not use most of them for the final step.
- You should be able to tell where the pipeline failed clearly, so you know from which step you should rerun the pipeline.
- You have to provide clear instructions on how to run the whole pipeline. The easier the better.
- You must provide evidence that the process has been completed successfully, i.e. you must provide a csv or json with the result of the query described above.

#### Not Met
- You should assume that it will run for different days, everyday.
- Folder path must have a date in it`s path.
  
## Observations

* **Challenges faced:**
  - Learning Airflow and Meltano and their extensions
  - Setting up the environment
* **Potential improvements:**
  - Use Airflow integrated with Meltano, as an orchestrator
  - Perhaps create a custom extension from the tap-csv extension to give the option of putting the current date in the output path of the file. I've seen that it's possible to implement our own extensions.

## Conclusion

In the end, the experience was positive, because the learning was invaluable.
I believe that, given the time I had and the amount of things I had to study, I was able to arrive at a satisfactory delivery value, even if I couldn't meet all the requirements.
