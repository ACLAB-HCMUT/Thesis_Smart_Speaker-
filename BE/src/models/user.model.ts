import mongoose from "mongoose";
import bcrypt from "bcrypt";
import config from "config";


export interface UserInput {
  email: string;
  name: string;
  password: string;
}


export interface UserDocument extends mongoose.Document, UserInput {
  createdAt: Date;
  updatedAt: Date;
  devices: string[];
  comparePassword(candidatePassword: string): Promise<boolean>;
}

// Định nghĩa schema
const userSchema = new mongoose.Schema<UserDocument>(
  {
    email: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    password: { type: String, required: true },
    devices: { type: [String], default: [] },
  },
  {
    timestamps: true,
  }
);

// Middleware pre-save
userSchema.pre("save", async function (next) {
  const user = this as UserDocument;

  // Nếu mật khẩu không thay đổi, bỏ qua
  if (!user.isModified("password")) {
    return next();
  }

  // Hash mật khẩu
  const salt = await bcrypt.genSalt(config.get<number>("saltWorkFactor"));
  user.password = await bcrypt.hash(user.password, salt);

  next();
});

// Phương thức so sánh mật khẩu
userSchema.methods.comparePassword = async function (
  candidatePassword: string
): Promise<boolean> {
  const user = this as UserDocument;
  return bcrypt.compare(candidatePassword, user.password).catch(() => false);
};

// Tạo model
const UserModel = mongoose.model<UserDocument>("User", userSchema);

export default UserModel;
