# UK Biobank Visualization etc.

## Dataset

### Format of data fields in UK Biobank

A data-field is the fundamental block of data held within the UK Biobank. It identifies the results of a question, measuremen or result. For more information about data fields and their basic properties, visit the official UK Biobank documentation.

Data fields in UK Biobank present the following structure:

                    f.XXXXX.X.X
                    f.field.instance.array

Field: The field number uniquely identifies the question, measurement or result in the data showcase.

Instance: The instance refers the assessment instance or visit. All participants attended an initial assessment centre (instance = 0), but a proportion were also invited several years later to repeat some of the assessments (instances 1 to 3).

Array: The array captures multiple answers that may be given to the same question.

Following the example in Table 1, the three fields (f.22040, f.42038 and f.42037) refer to the initial assessment visit (Instance = 0) and only one item of data is present for each participant (array = 0). A colour coded version of the previous .tab file example is presented in Table 2.


In order to build and run scala project, run the following:

"""bash
sbt compile
sbt run
"""

Note that the script is setup to write a CSV, and that because you're using Spark, this will be saved in partitions. Can merge these in different ways, but assuming that the data is coalesced into a single CSV with title ***.csv, can run the following:

"""bash

"""