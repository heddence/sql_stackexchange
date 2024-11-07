# Use the official Miniconda3 image as the base
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Copy the environment.yml file
COPY environment.yml .

# Install the Conda environment
RUN conda env create -f environment.yml

# Activate the environment and ensure it's available
ENV PATH /opt/conda/envs/sql_stackexchange/bin:$PATH

# Copy the application code
COPY app ./app
COPY sql_queries ./app

# Copy the entrypoint script
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port
EXPOSE 8000

# Set the entrypoint to activate the Conda environment
ENTRYPOINT ["./entrypoint.sh"]

# Set the command to run your application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
