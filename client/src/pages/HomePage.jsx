// import { Button } from '@/components/ui/button'
// import { Card, CardContent } from '@/components/ui/card'
// import React from 'react'
// import { Link } from 'react-router-dom'

// const HomePage = () => {
//     return (
//         <div className='h-screen w-screen flex justify-center items-center'>
//             <Card className="pt-5">
//                 <CardContent>
//                     <h1 className='text-center text-2xl font-bold mb-5'>Welcome To Mern Authentication</h1>
//                     <div className='flex justify-center gap-10'>
//                         <Button>
//                             <Link to="/login">Login</Link>
//                         </Button>
//                         <Button>
//                             <Link to="/register">Register</Link>
//                         </Button>
//                     </div>
//                 </CardContent>
//             </Card>
//         </div>
//     )
// }

// export default HomePage

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import React from 'react'
import { Shield, Lock, UserPlus, Sparkles } from 'lucide-react'

const HomePage = () => {
    return (
        <div className='min-h-screen w-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex justify-center items-center p-4 relative overflow-hidden'>
            {/* Animated background elements */}
            <div className='absolute inset-0 overflow-hidden'>
                <div className='absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse'></div>
                <div className='absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-1000'></div>
            </div>

            <Card className="relative z-10 pt-8 pb-8 px-6 backdrop-blur-sm bg-white/95 shadow-2xl border-0 max-w-md w-full">
                <CardContent className="space-y-6">
                    {/* Icon and Title Section */}
                    <div className='text-center space-y-3'>
                        <div className='flex justify-center mb-4'>
                            <div className='relative'>
                                <div className='absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full blur-lg opacity-50'></div>
                                <div className='relative bg-gradient-to-r from-purple-600 to-blue-600 p-4 rounded-full'>
                                    <Shield className='w-10 h-10 text-white' />
                                </div>
                            </div>
                        </div>
                        <h1 className='text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent'>
                            Welcome Back
                        </h1>
                        <p className='text-gray-600 text-sm'>
                            Secure authentication for your MERN application
                        </p>
                    </div>

                    {/* Features */}
                    <div className='grid grid-cols-2 gap-3 py-4'>
                        <div className='flex items-center gap-2 text-sm text-gray-600'>
                            <Sparkles className='w-4 h-4 text-purple-600' />
                            <span>Secure</span>
                        </div>
                        <div className='flex items-center gap-2 text-sm text-gray-600'>
                            <Lock className='w-4 h-4 text-purple-600' />
                            <span>Encrypted</span>
                        </div>
                    </div>

                    {/* Buttons */}
                    <div className='flex flex-col gap-3 pt-2'>
                        <Button 
                            asChild
                            className='w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 h-12'
                        >
                            <a href="/login" className='flex items-center justify-center gap-2'>
                                <Lock className='w-4 h-4' />
                                Login to Account
                            </a>
                        </Button>
                        <Button 
                            asChild
                            variant="outline"
                            className='w-full border-2 border-purple-600 text-purple-600 hover:bg-purple-50 transition-all duration-300 h-12'
                        >
                            <a href="/register" className='flex items-center justify-center gap-2'>
                                <UserPlus className='w-4 h-4' />
                                Create New Account
                            </a>
                        </Button>
                    </div>

                    {/* Footer */}
                    <p className='text-center text-xs text-gray-500 pt-4'>
                        Protected by enterprise-grade security
                    </p>
                </CardContent>
            </Card>
        </div>
    )
}

export default HomePage