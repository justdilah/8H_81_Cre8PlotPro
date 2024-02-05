import { createChatBotMessage } from "react-chatbot-kit";
import Panel from "../components/Panel/Panel";

const config = {
  botName:"Cre8Bot",
  initialMessages: [createChatBotMessage(`Hello world`)],
  state: {
    panels: []
  },
  widgets: [
    {
      widgetName: "panels",
      widgetFunc: (props) => <Panel {...props} />,
      mapStateToProps: ["panels"],
    }
  ]
}

export default config