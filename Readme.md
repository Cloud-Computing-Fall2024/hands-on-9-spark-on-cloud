## Hands-On #9: Working with AWS Services - EC2/Lightsail, S3, PySpark, and Docker

### Overview
In this hands-on session, you will complete two main tasks using AWS services:

1. **Task 1**: Create an EC2 or Lightsail VM, clone a GitHub repository containing a PySpark job, and run the PySpark job using input from an S3 bucket and outputting results back to the S3 bucket.
2. **Task 2**: Create a simple web server using Node.js and Docker, push the Docker image to a Docker registry, and run the container on the VM created in Task 1.

### Task 1: PySpark Job on AWS VM

#### Prerequisites
- AWS account with access to EC2 or Lightsail.
- IAM Role with permissions to access S3.
- PySpark installed on the VM.

#### Step-by-Step Instructions

1. **Create a VM (EC2 or Lightsail)**
   - Log in to your AWS Management Console.
   - Navigate to EC2 or Lightsail.
   - Create an Ubuntu VM instance with the necessary configurations (e.g., t2.micro).
   - Ensure the security group allows SSH and HTTP access.
   - Attach an IAM Role with permissions for S3.

2. **Connect to the VM**
   - Connect to your VM using SSH:
     ```bash
     ssh -i your-key.pem ubuntu@your-ec2-public-ip
     ```

3. **Install PySpark**
   - Run the following commands to install PySpark:
     ```bash
     sudo apt update
     sudo apt install openjdk-11-jdk -y
     sudo apt install python3-pip -y
     pip3 install pyspark
     ```

4. **Clone the GitHub Repository**
   - Clone the provided repository containing the PySpark job:
     ```bash
     git clone https://github.com/your-repo/your-spark-job.git
     cd your-spark-job
     ```

5. **Set Up AWS CLI (Optional)**
   - If not already configured, install and configure AWS CLI:
     ```bash
     sudo apt install awscli -y
     aws configure
     ```

6. **Run the PySpark Job**
   - Ensure your PySpark job reads input from an S3 bucket and writes output to S3:
     ```python
     from pyspark.sql import SparkSession

     spark = SparkSession.builder.appName("WordCountJob").getOrCreate()

     # Replace with your S3 bucket path
     input_path = "s3a://your-bucket/input.txt"
     output_path = "s3a://your-bucket/output/"

     # Read data from S3
     data = spark.read.text(input_path)
     words = data.selectExpr("split(value, ' ') as words").selectExpr("explode(words) as word")
     word_count = words.groupBy("word").count()

     # Write results back to S3
     word_count.write.csv(output_path, mode="overwrite", header=True)

     spark.stop()
     ```

   - Run the PySpark job on the VM:
     ```bash
     spark-submit word_count_job.py
     ```

#### Input and Output Files
- **Input File**: `input.txt` (store in your S3 bucket).
- **Output**: A folder with CSV files in the `s3a://your-bucket/output/`.

---

### Task 2: Node.js Web Server with Docker

#### Prerequisites
- Docker installed on your VM.
- Docker Hub account or any other Docker registry.

#### Step-by-Step Instructions

1. **Create a Simple Node.js Web Server**
   - Create a `server.js` file with the following code:
     ```javascript
     const express = require('express');
     const app = express();
     const port = 3000;

     app.get('/', (req, res) => {
       res.send('Hello, World! This is a simple Node.js web server running in a Docker container.');
     });

     app.listen(port, () => {
       console.log(`Server running at http://localhost:${port}`);
     });
     ```

2. **Create a `Dockerfile`**
   - Create a `Dockerfile` with the following content:
     ```Dockerfile
     # Use Node.js base image
     FROM node:14

     # Set working directory
     WORKDIR /app

     # Copy package files and install dependencies
     COPY package*.json ./
     RUN npm install

     # Copy the rest of the application code
     COPY . .

     # Expose the port and run the server
     EXPOSE 3000
     CMD ["node", "server.js"]
     ```

3. **Build and Push Docker Image**
   - Build your Docker image:
     ```bash
     docker build -t your-dockerhub-username/webserver:latest .
     ```

   - Log in to Docker Hub:
     ```bash
     docker login
     ```

   - Push the image:
     ```bash
     docker push your-dockerhub-username/webserver:latest
     ```

4. **Run Docker Container on AWS VM**
   - Pull the image on the VM:
     ```bash
     docker pull your-dockerhub-username/webserver:latest
     ```

   - Run the container:
     ```bash
     docker run -d -p 80:3000 your-dockerhub-username/webserver:latest
     ```

5. **Access the Web Server**
   - Visit `http://your-ec2-public-ip/` to see the web server running.

---

### Submission Guidelines
- Create a GitHub repository for your code and activity report.
- Commit and push your code, screenshots of your PySpark job output, and the web server running on the VM.
- Submit the GitHub repository link via [GitHub Classroom](https://classroom.github.com/a/22GFG33F).

---

### Evaluation Criteria
- **Task 1**: Successful completion of PySpark job on AWS VM with input and output from S3.
- **Task 2**: Deployment of the Dockerized web server and demonstration of it running on the VM.
- **Code Quality**: Clean, modular code with comments.
- **Documentation**: Clear steps and screenshots in the activity report.

Good luck with your hands-on activity!