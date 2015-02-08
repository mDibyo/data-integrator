__author__ = 'dibyo'


import rospy


class ROSNode(object):
    def __init__(self, name, **kwargs):
        """

        :param name: the name of the node
        :param anonymous: whether the node is anonymous
        :return:
        """
        self.name = name
        self.anonymous = kwargs.get('anonymous', False)

        rospy.init_node(self.name, anonymous=self.anonymous)

    @staticmethod
    def spin():
        rospy.spin()


class TopicSubscriberNode(ROSNode):
    def __init__(self, name, topic, msg_type, **kwargs):
        """

        :param name: the name of the node
        :param topic: the topic to subscribe to
        :param msg_type: type of messages in the topic
        :param callback: function/method to be called on topic
        :param callback_args: addition args to be passed to callback
        :param anonymous: whether the node is anonymous
        """
        super(TopicSubscriberNode, self).__init__(name, **kwargs)

        self.topic = topic
        self.msg_type = msg_type
        self.last_msg = None

        # Handle callback
        self.callback = self.callback_args = self.subscriber = None
        callback = kwargs.get('callback', None)
        if callback is not None:
            callback_args = kwargs.get('callback_args', None)
            self.add_callback(callback, callback_args)

    def add_callback(self, callback=None, callback_args=None, loginfo=False):
        """

        :param callback: the function to be called when there is a
            new message in the topic
        :param callback_args: addition args that must be passed to
            the callback
        :param loginfo: whether messages received should be logged
        """
        self.callback_args = callback_args
        self.callback = callback

        if callback is None:
            def callback(data):
                if loginfo:
                    rospy.loginfo(data)
            self.callback = callback
            self.callback_args = None

        self.subscriber = rospy.Subscriber(self.topic, self.msg_type,
                                           self._wrap_callback(callback),
                                           self.callback_args)

    def _wrap_callback(self, callback):
        def callback_wrapper(data, *args):
            self.last_msg = data
            return callback(data, *args)

        return callback_wrapper


class TopicPublisherNode(ROSNode):
    def __init__(self, name, topic, msg_type, **kwargs):
        """

        :param name: the name of the node
        :param topic: the topic to publish to
        :param msg_type: the type of messages in the topic
        :param anonymous: whether the node is anonymous
        :param wait_for_subscriber: whether the node should wait till
            there is a subscriber on the topic
        """
        super(TopicPublisherNode, self).__init__(name, kwargs)

        self.topic = topic
        self.msg_type = msg_type
        self.callback = kwargs.get('callback', None)

