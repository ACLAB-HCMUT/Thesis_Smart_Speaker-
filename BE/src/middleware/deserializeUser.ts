import { get } from "lodash";
import { Request, Response, NextFunction } from "express";
import { verifyJwt } from "../utils/jwt.utils";
import { reIssueAccessToken } from "../service/session.service";

const deserializeUser = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const accessToken = get(req, "headers.authorization", "").replace(/^Bearer\s/, "").trim();

  let refreshToken = get(req, "headers.x-refresh");

  if (Array.isArray(refreshToken)) {
    refreshToken = refreshToken[0]; // Lấy giá trị đầu tiên trong mảng
  }

  if (typeof refreshToken !== "string") {
    refreshToken = ""; // Đảm bảo refreshToken là chuỗi
  }

  if (!accessToken) {
    return next(); // Nếu không có accessToken, bỏ qua middleware
  }

  const { decoded, expired } = verifyJwt(accessToken, "accessTokenPublicKey");

  if (decoded) {
    res.locals.user = decoded;
    return next();
  }

  if (expired && refreshToken) {
    const newAccessToken = await reIssueAccessToken({ refreshToken });

    if (newAccessToken) {
      res.setHeader("x-access-token", newAccessToken);

      const result = verifyJwt(newAccessToken as string, "accessTokenPublicKey");

      if (result.decoded) {
        res.locals.user = result.decoded;
      }
    }
  }

  return next();
};

export default deserializeUser;
