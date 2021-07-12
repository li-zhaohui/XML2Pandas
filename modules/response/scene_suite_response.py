# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:17:53 2021

@author: m01winke
"""


class SceneSuiteResponse(dict):
    def as_xml(self):
        xml_string = "<ServerResponse>"

        # add channels
        for channel, parameters in self.items():
            xml_string += r"""<Channel id="{}">""".format(channel)

            # add parameters
            for parameter, value in parameters.items():

                if parameter == "FunctionValue":

                    xml_string += """<Parameter xsi:type="FunctionValue">"""

                    # add function values
                    for (
                        function_value_key,
                        function_value_value,
                    ) in value.items():

                        # TODO: can a function value be of type str? how do we have to parse it then?
                        if isinstance(function_value_value, int) or isinstance(
                            function_value_value, float
                        ):
                            xml_string += """<Expression expressionString="{}={}" />""".format(
                                function_value_key, function_value_value
                            )
                        else:
                            print("ERROR: unknown type for function value")

                    xml_string += "</Parameter>"

                else:
                    xml_string += (
                        r"""<Parameter xsi:type="{}" value="{}"/>""".format(
                            parameter, value
                        )
                    )

            xml_string += "</Channel>"

        xml_string += "</ServerResponse>\n"

        return xml_string
