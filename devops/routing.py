#-*- coding:utf-8 -*-
from channels import route_class, route
from devops.consumers import webterminal,SshTerminalMonitor

# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. In this example, we route
# all WebSocket connections to the class-based BindingConsumer (the consumer
# class itself specifies what channels it wants to consume)
channel_routing = [
    route_class(webterminal,path = r'^/ws'),
    route_class(SshTerminalMonitor,path= r'^/monitor/(?P<channel>\w+-\w+-\w+-\w+-\w+-\w+)'),
]