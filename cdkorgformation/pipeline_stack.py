from distutils.command.build import build
import aws_cdk as cdk
from aws_cdk import (
	aws_codecommit as codecommit,
	pipelines as pipelines,
	aws_codepipeline as codepipeline,
	aws_codepipeline_actions as codepipeline_actions,
	aws_codebuild as codebuild,
	aws_iam as iam,
)

from constructs import Construct

class CDKOrgFormationPipelineStack(cdk.Stack):

	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		# Create a codecommit repository called 'Organization Formation with CodePipeline built with CDK'
		repo = codecommit.Repository(
			self, 'CDKOrgFormation',
			repository_name='CDKOrgFormation'
		)

		pipeline = codepipeline.Pipeline(
			self, 'OrgFormationPipeline',
			pipeline_name='OrgFormationPipeline'
		)

		source_output = codepipeline.Artifact()
		source_action = codepipeline_actions.CodeCommitSourceAction(
			action_name="CodeCommit",
			repository=repo,
			output=source_output
		)

		pipeline.add_stage(
			stage_name="Source",
			actions=[source_action]
		)

		project = codebuild.PipelineProject(
			self, "BuildOrgFormation",
			build_spec=codebuild.BuildSpec.from_object(
				{
				"version": "0.2",
				"phases": {
					"build": {
					"commands": [
							"npm install -g aws-organization-formation",
							"echo installed aws-organization-formation",
							"org-formation -v",
							"org-formation update cdkorgformation/org.yml"	
							]
						}
						}
				}
			)
			)

		project.add_to_role_policy(
			iam.PolicyStatement(
					actions=['organizations:*'],
					sid='AllowOrganizationsAccess',
					effect=iam.Effect.ALLOW,
					resources=['*']
				)
		)

		project.add_to_role_policy(
			iam.PolicyStatement(
					actions=['s3:ListBucket'],
					sid='ListAccesstoOrgFormationBucket',
					effect=iam.Effect.ALLOW,
					resources=['arn:aws:s3:::organization-formation-123456789101'], # Update your Organization Account ID for the S3 bucket			
				)
		)

		project.add_to_role_policy(
			iam.PolicyStatement(
					actions=['s3:*'],
					sid='FullAccesstoOrgFormationBucket',
					effect=iam.Effect.ALLOW,
					resources=['arn:aws:s3:::organization-formation-123456789101/*'], # Update your Organization Account ID for the S3 bucket				
				)
		)

		project.add_to_role_policy(
			iam.PolicyStatement(
					actions=['events:PutEvents'],
					sid='PutEventsAccess',
					effect=iam.Effect.ALLOW,
					resources=['*'],					
				)
		)		

		build_action = codepipeline_actions.CodeBuildAction(
			action_name="CodeBuild",
			project=project,
			input=source_output,
		)


		pipeline.add_stage(
			stage_name="Build",
			actions=[build_action]
		)