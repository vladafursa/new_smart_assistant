import Message from "../components/Message";
import Form from "../components/Form";

const UserPanel = ({ chatMessages, onSend }) => {
  return (
    <div className="flex flex-col h-full">
      {chatMessages.map((chatMessage, i) => (
        <Message
          key={i}
          sender={chatMessage.sender}
          text={chatMessage.message}
        />
      ))}
      <div className="mt-auto">
        <Form sender="user" onSend={(text) => onSend(text, "user")} />
      </div>
    </div>
  );
};

export default UserPanel;
