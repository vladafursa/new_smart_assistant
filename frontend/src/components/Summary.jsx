const SummaryBox = ({ text }) => {
  return (
    <div className="flex flex-col bg-white border border-gray-300 rounded-lg shadow p-4">
      <label className="text-sm font-semibold text-gray-700 mb-2">
        Summary
      </label>

      <div className="bg-gray-50 text-gray-800 p-3 rounded-md min-h-20">
        {text || "There will be summary"}
      </div>
    </div>
  );
};

export default SummaryBox;
