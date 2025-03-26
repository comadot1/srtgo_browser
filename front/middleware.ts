// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export async function middleware(request: NextRequest) {

  if(process.env.USE_PASSCHECK?.toUpperCase() == "TRUE"){
    const expected = Buffer.from(`${process.env.ADMIN_PASSWORD}:${process.env.SECRET_KEY}`).toString('base64')
    const token = request.cookies.get('token')?.value

    if (!token && request.nextUrl.pathname == "/") {
      return NextResponse.redirect(new URL('/login', request.url))
    } else if (token && request.nextUrl.pathname == "/" && token != expected){
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  return NextResponse.next()
}


