# KVR Officer

Are you having a hard time getting an appointment from KVR? Don't worry, KVR officer is here to help! You can create a cron job that periodically checks if there are any appointments on the website and if there is, it sends you a message using a Telegram bot.

## Configuration

Minimal configuration with a `.env` file based on `.env.template` is required to link the Telegram bot to the running `kvr-officer`.

```
TELEGRAM_TOKEN=
USER_CHAT_ID=
APPOINTMENT_TYPE=CASETYPES[Niederlassungserlaubnis Blaue Karte EU - Beratung/ Antragstellung]
APPOINTMENT_NUMBER=1
```

### Telegram Token
A telegram token is created when defining a `/newbot` by messaging the `@BotFather`.

### User Chat ID
The desired `USER_CHAT_ID` can be found by messaging the newly created bot and querying its activity.

```shell script
https://api.telegram.org/bot{TOKEN}/getUpdates
```

### Appointment Type
Type of appointment based on `name` of CASETYPES of `.

### Appointment Quantity
(Optional) quantity of appointments. Defaults to `1`.
