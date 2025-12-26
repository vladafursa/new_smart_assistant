import { useRef, useState } from 'react'

const DropBox = () => {
  const uploadRef = useRef(null)  
  const [file, setFile] = useState(null)
  const [isDragOver, setIsDragOver] = useState(false)
  const [category, setCategory] = useState("")

  const handleChange = () => {
    setFile(uploadRef.current.files[0])
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setFile(e.dataTransfer.files[0])
    setIsDragOver(false)  
  }

  const handleUpload = async () => {
   if (!file || !category) {
    return console.warn("Choose category before upload");
    }

    const formData = new FormData()
    formData.append("file", file)
    formData.append("category", category)
    formData.append("author", "admin")
    const now = new Date().toLocaleString(); 
    formData.append("date-time", now);

    await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    })
  }

  return (
    <div className="mx-auto max-w-xl p-8 flex flex-col items-center space-y-6">
       {/* category selection*/}
       <div className="w-full">
        <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full rounded-md border border-gray-300 bg-white p-3 text-gray-700 shadow-sm 
                    focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition"
        >
            <option value="">-- Choose category --</option>
            <option value="customer"> Customer</option>
            <option value="technical"> Technical</option>
        </select>
        </div>


      {/* drop zone */}
      <div
        className={`w-full rounded-xl border-2 border-dashed border-gray-300 p-12 text-center cursor-pointer transition 
          hover:border-blue-500 hover:bg-blue-50 
          ${isDragOver ? 'opacity-70 border-blue-500 bg-blue-50' : ''}`}
        onClick={() => uploadRef.current.click()}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onDragLeave={() => setIsDragOver(false)}
      >
        <svg
          className="mx-auto h-14 w-14 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeWidth="2"
            d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M16 12l-4-4m0 0l-4 4m4-4v12"
          />
        </svg>
        <p className="mt-3 text-gray-600 font-medium">
          Click to choose or drag & drop file
        </p>

        <input
          ref={uploadRef}
          type="file"
          style={{ display: 'none' }}
          onChange={handleChange}
        />
      </div>

      {/* file name */}
      {file && (
        <p className="text-sm text-gray-700 font-medium">
          Selected file: <span className="font-semibold">{file.name}</span>
        </p>
      )}

      {/* upload button */}
      <button
        onClick={handleUpload}
       className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
      >
        Upload File
      </button>
    </div>
  )
}

export default DropBox