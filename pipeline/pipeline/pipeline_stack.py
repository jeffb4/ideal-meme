from aws_cdk import core as cdk

from aws_cdk import (
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_lambda as lambda_,
)


class PipelineStack(cdk.Stack):
    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        *,
        github_token: str = "",
        repo_name: str = "",
        lambda_code: lambda_.CfnParametersCode = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cdk_build = codebuild.PipelineProject(
            self,
            "CdkBuild",
            build_spec=codebuild.BuildSpec.from_object(
                dict(
                    version="0.2",
                    phases=dict(
                        install=dict(
                            commands=[
                                "npm install aws-cdk",
                                "npm update",
                                "python -m pip install poetry",
                                "cd pipeline",
                                "python -m poetry config virtualenvs.create false",
                                "python -m poetry install --no-root --no-dev",
                                "cd ..",
                            ]
                        ),
                        build=dict(commands=["cd pipeline", "npx cdk synth -o dist"]),
                    ),
                    artifacts={
                        "base-directory": "pipeline/dist",
                        "files": ["LambdaStack.template.json"],
                    },
                    environment=dict(buildImage=codebuild.LinuxBuildImage.STANDARD_5_0),
                )
            ),
        )
        lambda_build = codebuild.PipelineProject(
            self,
            "LambdaBuild",
            build_spec=codebuild.BuildSpec.from_object(
                dict(
                    version="0.2",
                    phases=dict(
                        install=dict(
                            commands=[
                                "cd lambda",
                                "npm install",
                                "npm install typescript",
                            ]
                        ),
                        build=dict(commands=["npx tsc index.ts"]),
                    ),
                    artifacts={
                        "base-directory": "lambda",
                        "files": ["index.js", "node_modules/**/*"],
                    },
                    environment=dict(buildImage=codebuild.LinuxBuildImage.STANDARD_5_0),
                )
            ),
        )
        github_token = cdk.CfnParameter(
            self,
            "githubToken",
            type="String",
            description="GitHub token for source access",
        )
        source_output = codepipeline.Artifact()
        cdk_build_output = codepipeline.Artifact("CdkBuildOutput")
        lambda_build_output = codepipeline.Artifact("LambdaBuildOutput")

        lambda_location = lambda_build_output.s3_location
        codepipeline.Pipeline(
            self,
            "Pipeline",
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        codepipeline_actions.GitHubSourceAction(
                            action_name="Checkout",
                            output=source_output,
                            owner="jeffb4",
                            repo="ideal-meme",
                            oauth_token=cdk.SecretValue.plain_text(
                                github_token.value_as_string
                            ),
                            trigger=codepipeline_actions.GitHubTrigger.WEBHOOK,
                        )
                        # codepipeline_actions.CodeCommitSourceAction(
                        #     action_name="CodeCommit_Source",
                        #     branch="main",
                        #     repository=code,
                        #     output=source_output,
                        # )
                    ],
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="Lambda_Build",
                            project=lambda_build,
                            input=source_output,
                            outputs=[lambda_build_output],
                        ),
                        codepipeline_actions.CodeBuildAction(
                            action_name="CDK_Build",
                            project=cdk_build,
                            input=source_output,
                            outputs=[cdk_build_output],
                        ),
                    ],
                ),
                codepipeline.StageProps(
                    stage_name="Deploy",
                    actions=[
                        codepipeline_actions.CloudFormationCreateUpdateStackAction(
                            action_name="Lambda_CFN_Deploy",
                            template_path=cdk_build_output.at_path(
                                "LambdaStack.template.json"
                            ),
                            stack_name="LambdaDeploymentStack",
                            admin_permissions=True,
                            parameter_overrides=dict(
                                lambda_code.assign(
                                    bucket_name=lambda_location.bucket_name,
                                    object_key=lambda_location.object_key,
                                    object_version=lambda_location.object_version,
                                )
                            ),
                            extra_inputs=[lambda_build_output],
                        )
                    ],
                ),
            ],
        )
