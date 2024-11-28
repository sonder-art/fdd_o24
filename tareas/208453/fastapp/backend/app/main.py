from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
from io import StringIO

app = FastAPI()

# Store the uploaded DataFrame in memory
video_data = None

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV file containing video-related data.
    Expected columns: 'video_id', 'view_count', 'duration', 'likes', etc.
    """
    global video_data
    try:
        content = await file.read()
        video_data = pd.read_csv(StringIO(content.decode("utf-8")))
        return {"message": "File uploaded successfully", "columns": video_data.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to upload file: {e}")

@app.get("/columns/")
async def get_columns():
    """
    Retrieve a list of available columns in the uploaded data.
    """
    if video_data is None:
        raise HTTPException(status_code=404, detail="No data available")
    return {"columns": video_data.columns.tolist()}

class ColumnRequest(BaseModel):
    column: str

@app.post("/statistics/")
async def get_statistics(request: ColumnRequest):
    """
    Retrieve basic statistics for a specific column, such as 'view_count' or 'duration'.
    """
    if video_data is None:
        raise HTTPException(status_code=404, detail="No data available")
    
    column = request.column
    if column not in video_data.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    
    if pd.api.types.is_numeric_dtype(video_data[column]):
        stats = {
            "max": video_data[column].max(),
            "min": video_data[column].min(),
            "mean": video_data[column].mean(),
            "median": video_data[column].median(),
            "quantiles": video_data[column].quantile([0.25, 0.5, 0.75]).to_dict()
        }
        return stats
    else:
        return {"message": "Not a numeric column"}

@app.get("/video/{video_id}/statistics/")
async def get_video_statistics(video_id: str):
    """
    Retrieve statistics for a specific video by its ID.
    """
    if video_data is None:
        raise HTTPException(status_code=404, detail="No data available")

    if 'video_id' not in video_data.columns:
        raise HTTPException(status_code=404, detail="No 'video_id' column found")

    video_info = video_data[video_data['video_id'] == video_id]
    if video_info.empty:
        raise HTTPException(status_code=404, detail="Video ID not found")

    # Sample stats on specific columns; customize based on available columns in your schema
    stats = {
        "view_count": video_info["view_count"].values[0] if "view_count" in video_info.columns else "N/A",
        "duration": video_info["duration"].values[0] if "duration" in video_info.columns else "N/A",
        "likes": video_info["likes"].values[0] if "likes" in video_info.columns else "N/A",
        "dislikes": video_info["dislikes"].values[0] if "dislikes" in video_info.columns else "N/A"
    }
    return stats

