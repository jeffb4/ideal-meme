from aws_cdk import core as cdk

from aws_cdk import (
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_lambda as lambda_,
)


class PipelineStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
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
                                "python -m pip install -r requirements.txt",
                            ]
                        ),
                        build=dict(commands=["npx cdk synth -o dist"]),
                    ),
                    artifacts={
                        "base-directory": "dist",
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
