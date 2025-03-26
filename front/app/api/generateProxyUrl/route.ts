import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
    const expected = Buffer.from(`${process.env.ADMIN_PASSWORD}:${process.env.SECRET_KEY}`).toString('base64')

    if(request.cookies.get('token')?.value != expected){
        return NextResponse.json({ url: "" })
    }

    return NextResponse.json({ url: process.env.NEXT_PUBLIC_SOCKET_PROXY + "?token=" + expected})
}
