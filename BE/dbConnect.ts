import mongoose from 'mongoose';

const DB_ENDPOINT = 'mongodb+srv://locphan2113971:choancuc123@cluster0.fll8b.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=Cluster0';

mongoose.connect(DB_ENDPOINT)
    .then(() => console.log("Connected to MongoDB"))
    .catch((error: Error) => console.error("MongoDB connection error:", error));

export default mongoose;
