﻿# pythonaws-project
Project is based on AWS -> Lambda Functions -> EC2 Instances and Snapshots -> Main code is based on Python

Goal to achieve:
1. A lamda function 
2. Fetch all EBS Snapshots
3. Filter out EBS Snapshots and delete the stale EBS Snapshots
4. From event scheduler make it automatically

Steps required:
1. EC2 Instances
2. Create a Snapshots
3. Create lamda function
4. Change execution role and time to 10sec
5. Test it with different parameters
6. Make it automatic using event scheduler

Note: This project is inspired by Abhishek Veeramalla Python for devops playlist:
https://www.youtube.com/watch?v=3ExnySHBO6k
