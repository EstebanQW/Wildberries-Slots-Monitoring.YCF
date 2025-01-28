from wb_calendar import main


def handler(event, context):
    return {
        "statusCode": 200,
        "body": main(),
    }
