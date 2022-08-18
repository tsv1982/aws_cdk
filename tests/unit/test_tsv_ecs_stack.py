import aws_cdk as core
import aws_cdk.assertions as assertions

from tsv_ecs.tsv_ecs_stack import TsvEcsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in tsv_ecs/tsv_ecs_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TsvEcsStack(app, "tsv-ecs")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
