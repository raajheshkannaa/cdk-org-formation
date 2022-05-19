# Manage AWS Organizations with Code 🚀
⭐️ Organization Formation ⭐️ built by Olaf Conijn is an amazing tool which helps simplify the process of managing AWS Organizations 🥇

https://github.com/org-formation/org-formation-cli

🔥 We have wrapped `org-formation-cli` within a CDK App which deploys a CodePipeline pipeline which will auto manage AWS Organization.
Some of the common tasks we could 
* Create Organization Units
* Move Accounts between OUs
* Create AWS New Accounts
* Manage Service Control Policies for OUs/Accounts
* Manage Account Contacts, IAM Aliases, etc..


[![Manage AWS Organizations as Code](https://img.youtube.com/vi/Q8cARqxV1Iw/0.jpg)](https://www.youtube.com/watch?v=Q8cARqxV1Iw)


## Usage
This is a CDK Project, which means you need to have CDK installed on your local system with `npm i -g aws-cdk`
### Steps
> git clone https://github.com/raajheshkannaa/cdk-org-formation-pipeline
* Update the organization account id in the `cdkorgformation/pipeline_stack.py`, which is the s3 bucket permissions where org-formation will hold the org structure in its state.json file.
* Install org-formation-cli by running `npm install -g aws-organization-formation`
* Change directory into the `cdkorgformation` folder which holds a dummy org.yml file for reference.
* From this directory, initialize the Org Structure by running `org-formation init org.yml --region us-east-1`. This will overwrite the current dummy `org.yml` file with your actual AWS Organizations structure.
> cdk deploy --profile aws-org-profile
* This will create the codecommit repository and the CodePipeline with the right permissions and .yml file into the AWS Organizations Account.
* Configure your local git client to work with the newly created CodeCommit repository.
* Push the code to the CodeCommit repository to kick off the codepipeline.
* This will run the `org-formation update cdkorgformation/org.yml` command which will essentially make the changes you'd like to make to the AWS Organization structure.

**Note**: Every time you want to update or make changes to your Organization structure, such as create accounts or manage OUs, run `org-formation init org.yml --region us-east-1` locally in the `<cdk app>/cdkorganization/` folder, before making and pushing those changes to the code repository.

## Considerations
* We could use the option of building a pipeline which OrgFormation would build for us with the `org-formation init-pipeline` command, however because we build our own pipeline and most of our automation's are built with CDK, we resort to manage OrgFormation with CDK, instead of having OrgFormation manage our CDK or Serverless apps, which are features provided by the tool built by Olaf.
* Org Formation offers so much more, such as tasks which could be carried out once an account is created, such as enable CloudTrail, GuardDuty and any other CloudFormation template you'd want to run in the new account. Examples here - https://github.com/org-formation/org-formation-cli/tree/master/examples
* Again we don't use these features of org-formation, because most of the automation on new accounts is setup with CDK already long before, so we will continue to use that, while use `org-formation-cli` only for managing the hierarchy or overall structure of the Organizations itself.

## Attributions
Heavily derived from [AWS Organization Formation](https://github.com/org-formation/org-formation-cli), built by Olaf Conijn.

Checkout this video to learn more: https://www.youtube.com/watch?v=mLAGHzidHJ0
