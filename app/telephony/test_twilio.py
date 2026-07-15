from app.telephony.twilio_client import TwilioClient

def main():

    client = TwilioClient()

    result = client.make_call(
        "+910000000000"      # Customer mobile number
    )

    print(result)


if __name__ == "__main__":
    main()