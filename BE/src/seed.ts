import mongoose from 'mongoose';
import Device from './models/devices.model'; 

const DB_ENDPOINT = 'mongodb+srv://locphan2113971:choancuc123@cluster0.fll8b.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=Cluster0';

// Kết nối tới MongoDB
mongoose.connect(DB_ENDPOINT)
    .then(() => console.log('Connected to MongoDB'))
    .catch((error: Error) => console.error('MongoDB connection error:', error));

// Dữ liệu mẫu
const seedDevices = [
    {
        adaFruitID: '123456',
        deviceName: 'Đèn 1',
        deviceState: 'OFF',
        deviceType: 'led1',
        userID: "6741f4d371f94fc0bc20becc",
        schedule: [],
        color: 'white',
        minLimit: 0,
        maxLimit: 0,
        lastValue: 0,
        updatedTime: new Date().toISOString(),
        environmentValue: []
    },
    {
        adaFruitID: '654321',
        deviceName: 'Quạt',
        deviceState: 'OFF',
        deviceType: 'fan',
        userID: null,
        schedule: [],
        color: 'white',
        minLimit: 0,
        maxLimit: 0,
        lastValue: 0,
        updatedTime: new Date().toISOString(),
        environmentValue: []
    }
];

// Hàm chạy seed
const runSeed = async () => {
    try {
        // Xóa toàn bộ dữ liệu cũ trong collection devices
       
        // Thêm dữ liệu mẫu
        const devices = await Device.insertMany(seedDevices);
        console.log(`${devices.length} devices added to the database.`);

        // Đóng kết nối
        mongoose.connection.close();
    } catch (error) {
        console.error('Error seeding data:', error);
        mongoose.connection.close();
    }
};

runSeed();
