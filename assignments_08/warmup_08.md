## Cloud Concepts

<!-- Q1 -->

### What is the core economic model of cloud computing, and how does it differ from owning your own servers?

- Cloud computing means using someone else's computer over the internet instead of running it on your own local machine or in your own data center. Therefore it provide you with services that and capacity that your local machine is not able to perform, store, or execute. To achieve a cloud computing at a local level will require infrastructure and that is impossible for an individual to do or make it happen.

<!-- Q2 -->

### What is the difference between vertical scaling and horizontal scaling? Give a concrete example of when you might choose each.

- Vertical scaling is a matter of adding resources when traffic or more resources are needed. Adding more RAm, more GPU, and so on. It is ideal to use vertical scaling when an application cannot run on multiple machine and buying a larger server will be easier.
- Horizontal scaling is cloning a machine to multiple machine to fit the incoming traffic. A good example of this is when a website is getting significant amount of traffic all at once, cloning the machine and help of a Load Balancer you cant prevent your site from going down.

### Then, for the three scenarios below, write one sentence saying which type of scaling applies and why.

A web app that normally handles 1,000 users per day suddenly needs to handle 100,000 after a viral product launch.

- Horizontal scaling because it is a significant traffic increase and since it is temporary, cloning machines to support the increase in traffic and then later remove them will be ideal.

A data scientist's model training job is running too slowly, and they want a machine with a faster GPU and more RAM

- Vertical scaling, because you can just add more resources on top of the existing one, in this case more RAM and GPU

A data pipeline that processes 10 files per run now needs to process 10,000 files per run, and the work can be split across machines.

- horizontal scaling, because of it capability to split work across different machines

<!-- Q3 -->

### Before writing your definitions, classify each item in the list below as IaaS, PaaS, SaaS, or BaaS. One sentence of reasoning is enough for each.

- Gmail -> SaaS, it is a complete application delivered vai the internet
- Azure Virtual Machines -> IaaS , it is used to manage the operation system and application on organization or individual level
- AWS S3 (Simple Storage Service) -> IaaS, S3 does not require server, disk , or operation system management.
- GitHub Codespaces -> PaaS, it manages the infrastructure and operation system, an you just run you application
- Snowflake -> SaaS, you do not provision , configure , or manage servers, hardware , or underlying cloud resources.
- Supabase -> BaaS, it provides a ready-to-use backend features on top of PostgresSQL

#### Now describe IaaS, PaaS, and SaaS in your own words. For each, give one example (from the lesson or the list above) and describe what you, as the developer, are responsible for managing.

- IaaS services gives you infrastructure (server, storage, networking), and you manage the operating system and applications. Example Azure Virtual Machine
- PaaS services manages the infrastructure and OS, you only focus on your application code. Example Heroku, you upload you code and they will deal with deploying it running it.
- SaaS services is a complete application delivered over the internet. Example, GMail, an email provider, you just use it and manage what to keep and what to delete.

<!-- Q4 -->

### What is a managed data platform like Databricks or Snowflake, and how does it differ from using a cloud provider like AWS or GCP directly? What do you gain, and what do you give up?

- Manage date platform pre-wire the piece for you, optimizing specifically for data and analytics workloads unlike cloud provider that require configuring and offer dozen of services.
- Manage sata Platform are usual configure for a specific service while Cloud provider are more complex, including dozens of services
- Manage data platform provide you with easy way to get started with cloud provider without the hustle of figuring out the configures, design to get your app running as fast as possible. What you give up is the capability to have full control of the service, since most everything is configured for you.

<!-- Q5 -->

### The lesson describes a situation where the cloud is probably not the right choice. What is that situation?

- If your dataset fits comfortably on a single machine and you do not have massive compute demands, local processing is often faster and cheaper. This is often the best approach when setting up an initial prototype.

<!-- Cloud Landscape -->

<!-- Q1 -->

### Name the three hyperscalers. For each, write one sentence describing its primary strength and the type of organization most likely to use it.

- _Amazon Web Services (AWS)_ -> Has the broadest service catalog of any provider. If you're working in a large enterprise, a startup, or a nonprofit with engineering staff, AWS is probably in the mix.
- _Google Cloud Platform (GCP)_ -> Strongest in data and machine learning and If you're working on large-scale analytics or ML infrastructure, GCP is often the preferred environment
- _Microsoft Azure_ -> is the dominant provider in enterprise and government settings, largely because of its deep integration with Windows, Active Directory, and Microsoft 365; making it ideal large nonprofits and public-sector organizations are already Azure customers through existing Microsoft agreements.

<!-- Q2 -->

### The lesson explains why this course switched from Microsoft Azure to Supabase. It gives three concrete reasons. Summarize each reason in your own words — one sentence each.

- _Access_ -> Azure requires a organization provisioning, which makes it harder to access and permissions while Supabase is a self-provisioned.
- _Pedagogical fit_ -> Supabase stores data as column and rows in a relational database, make it easier to transfer (querying, filtering and so on) while Azure stores data in opaque files which require file path to access.
- _Pipeline coherence_ -> The table that will be working on have a clear relationship between them, making it a better choice as we can inspect and debug clearly.

### Taxonomy

- You need to store 10 TB of image files and retrieve them by filename from any machine. -> Object Storage -> S3
- You need to run an ML training job on a GPU for four hours, then shut it down. -> ML Platform -> SageMaker
- You need to host a web API that automatically scales up when traffic spikes and scales down when it quiets. -> Serverless compute -> Lambda
- You need to send structured data to a large language model and get a text response back. -> LLM API -> Bedrock

<!-- Q4 -->

### The lesson says most projects don't use one provider for everything. Describe a simple data project of your own design (one or two sentences is fine) and sketch a plausible stack using services from at least two different providers or products from the taxonomy table. Then answer: is there a benefit to consolidating to one provider, and what would you give up if you did?

- A Fullstack project that uses AI to predict the weather for a user, it needs a data, a place to train the model and A UI.

- Web App -> EC2 <-> Azure ML <-> BigQuery

- The benefit to consolidate to one is having all in one roof, being able to control/ configure everything in one spot.

- What you will be giving up is accessibility to some feature like BigQuery, which is fully serverless, automated storage optimization and so on. It comes do on what you are working on because every project requires something different.
