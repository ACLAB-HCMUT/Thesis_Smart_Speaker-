import jwt from "jsonwebtoken";
import config from "config";

export function signJwt(
    object: Object,
    keyName: "accessTokenPrivateKey" | "refreshTokenPrivateKey",
    options?: jwt.SignOptions
  ) {
    // Lấy private key trực tiếp từ config
    const signingKey = config.get<string>(keyName);
  
    // Sử dụng private key không qua Buffer xử lý
    return jwt.sign(object, signingKey, {
      ...(options && options),
      algorithm: "RS256", // Đảm bảo sử dụng đúng thuật toán
    });
  }
  export function verifyJwt(
    token: string,
    keyName: "accessTokenPublicKey" | "refreshTokenPublicKey"
  ) {
    // Lấy public key trực tiếp từ config
    const publicKey = config.get<string>(keyName);
  
    try {
      const decoded = jwt.verify(token, publicKey);
      return {
        valid: true,
        expired: false,
        decoded,
      };
    } catch (e: any) {
      console.error(e);
      return {
        valid: false,
        expired: e.message === "jwt expired",
        decoded: null,
      };
    }
  }