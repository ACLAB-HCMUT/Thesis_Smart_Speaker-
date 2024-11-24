import { Request, Response } from "express";
import mongoose from "mongoose"; 

import config from "config";
import {
  createSession,
  findSessions,
  updateSession,
} from "../service/session.service";
import { validatePassword } from "../service/user.service";
import { signJwt } from "../utils/jwt.utils";

export async function createUserSessionHandler(req: Request, res: Response) {
    const user = await validatePassword(req.body);
  
    if (!user) {
      return res.status(401).send("Invalid email or password");
    }
  
    // Sử dụng Type Assertion để xác nhận kiểu
    const userId = (user._id as mongoose.Types.ObjectId).toString();
  
    // Tạo session
    const session = await createSession(userId, req.get("user-agent") || "");
  
    // Tạo access token
    const accessToken = signJwt(
      { ...user.toJSON(), session: session._id.toString() },
      "accessTokenPrivateKey",
      { expiresIn: config.get<string>("accessTokenTtl") } // 15 minutes
    );
  
    // Tạo refresh token
    const refreshToken = signJwt(
      { ...user.toJSON(), session: session._id.toString() },
      "refreshTokenPrivateKey",
      { expiresIn: config.get<string>("refreshTokenTtl") } // 1 day
    );
  
    return res.send({ accessToken, refreshToken });
  }
  
export async function getUserSessionsHandler(req: Request, res: Response) {
  const userId = res.locals.user._id;

  const sessions = await findSessions({ user: userId, valid: true });

  return res.send(sessions);
}

export async function deleteSessionHandler(req: Request, res: Response) {
  const sessionId = res.locals.user.session;

  await updateSession({ _id: sessionId }, { valid: false });

  return res.send({
    accessToken: null,
    refreshToken: null,
  });
}