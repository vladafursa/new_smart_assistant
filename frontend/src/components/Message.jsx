const Message = ({ sender, text }) => {
  const isUser = sender === "user";

  return (
    <div className={`flex flex-col mb-3 ${isUser ? "items-start" : "items-end"}`}>
      <span className="text-xs text-gray-500 mb-1">{sender}</span>
      <div
        className={`px-4 py-2 rounded-lg shadow max-w-md ${
          isUser ? "bg-purple-700 text-white" : "bg-gray-500 text-white"
        }`}
      >
        {text}
      </div>
      <span className="text-[10px] text-gray-400 mt-1">22:40</span>
    </div>
  );
};

export default Message;