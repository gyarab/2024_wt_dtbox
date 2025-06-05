import machine, ubinascii

from umqtt.robust import MQTTClient as MQTTClientOrig


client_id = ubinascii.hexlify(machine.unique_id()).decode()
# c = MQTTClient(client_id, "192.168.84.246", ssl=0)   # change this
# c = MQTTClient(client_id, "mqtt.hivemq.com", ssl=0)   # change this
class MQTTClient(MQTTClientOrig):
    @classmethod

    def from_config(cls):
        """
        Creates MQTTClient instance with values saved in config

        :raises: :class:`RuntimeError`: Config is invalid

        :returns: :class:`MQTTClient` instance
        :rtype: MQTTClient
        """
        from dtbox.config import get_config

        config = get_config()

        try:
            iconfig = config['mqtt']
        except KeyError:
            raise RuntimeError('MQTT config is not set')

        values = {
            'client_id': client_id
        }

        # must be in same order as in constructor!
        fields = ['server', 'port', 'user', 'password', 'keepalive', 'ssl']
        invalid_fields = []
        for key in fields:
            try:
                values[key] = iconfig[key]
            except KeyError:
                invalid_fields.append(key)

        if len(invalid_fields) > 0:
            raise RuntimeError(f'MQTT config fields are not set: {", ".join(invalid_fields)}')

        return cls(**values)        
        



