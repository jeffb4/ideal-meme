from aws_cdk import (
    core,
    aws_codedeploy as codedeploy,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
import datetime


class LambdaStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs):
        super().__init__(app, id, **kwargs)

        self.lambda_code = lambda_.Code.from_cfn_parameters()

        func = lambda_.Function(
            self,
            "Lambda",
            code=self.lambda_code,
            handler="index.main",
            runtime=lambda_.Runtime.NODEJS_10_X,
            description="Function generated on {}".format(datetime.datetime.now()),
        )

        alias = lambda_.Alias(
            self, "LambdaAlias", alias_name="Prod", version=func.current_version
        )

        codedeploy.LambdaDeploymentGroup(
            self,
            "DeploymentGroup",
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
        )
        api = apigateway.RestApi(
            self,
            "ideal-meme-api",
            rest_api_name="Ideal Meme Service",
            description="This service serves epoch.",
        )

        ideal_meme_integration = apigateway.LambdaIntegration(
            func, request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method("GET", ideal_meme_integration)

        core.CfnOutput(self, "APIG", description="API Gateway URL", value=api.url)
