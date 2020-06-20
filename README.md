# From Amazon Mechinal Turk to Yolo

## Introduction

[Amazon Mechanical Turk (MTurk)](https://www.mturk.com/) is a crowdsourcing marketplace that makes it easier for individuals and businesses to outsource their processes and jobs to a distributed workforce who can perform these tasks virtually. This could include anything from conducting simple data validation and research to more subjective tasks like survey participation, content moderation, and more. MTurk enables companies to harness the collective intelligence, skills, and insights from a global workforce to streamline business processes, augment data collection and analysis, and accelerate machine learning development.

The batch job generates a CSV containing the following headers:

| Field | Type |
|-------|------|
| HITId | String |
| HITTypeId | String |
| Title | String |
| Description | String |
| Keywords | String |
| Reward | String |
| CreationTime | String |
| MaxAssignments | String |
| RequesterAnnotation | String |
| AssignmentDurationInSeconds | String |
| AutoApprovalDelayInSeconds | String |
| Expiration | String |
| NumberOfSimilarHITs | String |
| LifetimeInSeconds | String |
| AssignmentId | String |
| WorkerId | String |
| AssignmentStatus | String |
| AcceptTime | String |
| SubmitTime | String |
| AutoApprovalTime | String |
| ApprovalTime | String |
| RejectionTime | String |
| RequesterFeedback | String |
| WorkTimeInSeconds | String |
| LifetimeApprovalRate | String |
| Last30DaysApprovalRate | String |
| Last7DaysApprovalRate | String |
| Input.image_url | String |
| Answer.annotatedResult.boundingBoxes | JSON |
| Answer.annotatedResult.inputImageProperties.height" | String |
| Answer.annotatedResult.inputImageProperties.width" | String |
| Approve | String |
| Reject | String |

The aim of this repository is, based on this CSV structure, generate the following folder structure

```bash
dataset/               # Dataset for training on Yolo
└── backup/            # Stores backup weight files during the training process
└── images/            # Stores the jpeg images
    ├── 1.jpeg         # RGB Image
    └── 2.jpeg
└── labels/            # Store the image annotations
    ├── 1.txt          # Image annotations
    └── 2.txt
├── test.txt           # List of images paths to be used in the validation process
├── train.txt          # List of images paths to be used in the training process
├── configuration.data # A configuration file required by Darknet
└── classes.names      # A file which does the translation between classes ids to their names

```

### [Image annotation format](https://github.com/AlexeyAB/Yolo_mark/issues/60)

`.txt`-file for each `.jpg`-image-file - in the same directory and with the same name, but with `.txt`-extension, and put to file: object number and object coordinates on this image, for each object in new line: `<object-class> <x> <y> <width> <height>`

Where:

-   `<object-class>` - integer number of object from 0 to (classes-1)
-   `<x> <y> <width> <height>` - float values relative to width and height of image, it can be equal from (0.0 to 1.0]
-   for example: <x> = <absolute_x> / <image_width> or <height> = <absolute_height> / <image_height>
-   atention: <x> <y> - are center of rectangle (are not top-left corner)

For example for `img1.jpg` you will be created `img1.txt` containing:

```
1 0.716797 0.395833 0.216406 0.147222
0 0.687109 0.379167 0.255469 0.158333
1 0.420312 0.395833 0.140625 0.166667
```

### Example of `configuration.data`

```bash
classes = 2
train = /home/dataset/train.txt
valid = /home/dataset/test.txt
names = /home/dataset/classes.names
backup = /home/dataset/backup/
```

### Example of `classes.names`

```bash
cat
dog
```

## Requirements
<!--
### Easiest

Use [Docker](https://docs.docker.com/docker-for-windows/install/)

### Hard

Note: this process is described for a Debian-based Linux distribution (Debian, Ubuntu, Mint, etc), if you use Windows or any other operating system, read the comments over the commands and adapt them to your environment
-->

```bash
# Install python3 and pip3
$ apt update && apt install python3 python3-pip -y

# Install Python dependencies
$ pip3 install -r requirements.txt
```

<!-- ## Build

### Docker

```bash
$ docker image build -t "from-amazon-mturk-to-yolo" .
```

### Manual -->

## Usage

<!-- ### Docker

```bash
$ docker container run -v $(pwd):/dataset from-amazon-mturk-to-yolo
```

### Manual -->

```bash
$ python3 src/converter.py --csv=/home/user/batch_results.csv
```

## LICENSE

MIT License

Copyright (c) 2019 Claudio Busatto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
