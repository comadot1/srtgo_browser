import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    const body = await request.json()
    const password = body.password

    const isValid = password === process.env.ADMIN_PASSWORD

    if (isValid) {

        const referer = request.headers.get('referer') || request.url
        const origin = new URL(referer).origin
        const protocol = new URL(referer!).protocol

        const hashedToken = Buffer.from(`${password}:${process.env.SECRET_KEY}`).toString('base64')

        const response = NextResponse.redirect(origin)
        response.cookies.set('token', hashedToken, {
            httpOnly: true,
            secure: protocol.includes("https")?true:false,
            sameSite: 'lax',
            path: '/',
            maxAge: 60 * 60 * 3, // 3시간
        })

        return response
    } else {
        return NextResponse.json({ valid: isValid })
    }
}
