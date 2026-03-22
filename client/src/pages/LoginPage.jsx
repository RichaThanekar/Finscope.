// import { Button } from '@/components/ui/button'
// import React from 'react'
// import { Link, useNavigate } from 'react-router-dom'
// import { zodResolver } from "@hookform/resolvers/zod"
// import { useForm } from "react-hook-form"
// import { z } from "zod"
// import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
// import { Input } from '@/components/ui/input'
// import { toast } from '@/hooks/use-toast'

// const LoginPage = () => {
//     const baseUrl = import.meta.env.VITE_API_BASE_URL
//     const navigate = useNavigate()
//     const formSchema = z.object({
//         email: z.string().email(),
//         password: z.string().min(8, { message: "Password must be at least 8 characters." }),
//     })


//     const form = useForm({
//         resolver: zodResolver(formSchema),
//         defaultValues: {
//             email: '',
//             password: '',
//         },
//     })

//     const handleForm = async (values) => {
//         try {
//             const response = await fetch(`${baseUrl}/api/auth/login`, {
//                 method: 'Post',
//                 headers: { "Content-type": "application/json" },
//                 credentials: 'include',
//                 body: JSON.stringify(values)
//             })
//             const data = await response.json()
//             if (data.status) {
//                 toast({
//                     title: "Login Status!",
//                     description: data.message,
//                 })
//                 navigate('/dashboard')
//             } else {
//                 toast({
//                     title: "Login Status!",
//                     description: data.message,
//                     variant: "destructive"
//                 })
//             }

//         } catch (error) {
//             toast({
//                 title: "Login Status!",
//                 description: error.message,
//                 variant: "destructive"
//             })
//         }
//     }

//     return (
//         <div className="w-full grid grid-cols-1 md:grid-cols-2 min-h-screen">
//             <div className="flex items-center justify-center py-12">
//                 <div className="mx-auto grid w-[350px] gap-6">
//                     <div className="grid gap-2 text-center">
//                         <h1 className="text-3xl font-bold">Login</h1>
//                         <p className="text-balance text-muted-foreground">
//                             Enter your email below to login to your account
//                         </p>
//                     </div>
//                     <Form {...form}>
//                         <form onSubmit={form.handleSubmit(handleForm)} className="grid gap-4">
//                             <div className="grid gap-2">
//                                 <FormField
//                                     control={form.control}
//                                     name="email"
//                                     render={({ field }) => (
//                                         <FormItem>
//                                             <FormLabel>Email</FormLabel>
//                                             <FormControl>
//                                                 <Input placeholder="m@example.com" {...field} />
//                                             </FormControl>
//                                             <FormMessage />
//                                         </FormItem>
//                                     )}
//                                 />
//                             </div>
//                             <div className="grid gap-2">
//                                 <FormField
//                                     control={form.control}
//                                     name="password"
//                                     render={({ field }) => (
//                                         <FormItem>
//                                             <div className="flex items-center">
//                                                 <FormLabel>Password</FormLabel>
//                                                 <Link
//                                                     to="/forgot-password"
//                                                     className="ml-auto inline-block text-sm underline"
//                                                 >
//                                                     Forgot your password?
//                                                 </Link>
//                                             </div>
//                                             <FormControl>
//                                                 <Input type="password" {...field} />
//                                             </FormControl>
//                                             <FormMessage />
//                                         </FormItem>
//                                     )}
//                                 />
//                             </div>
//                             <Button type="submit" className="w-full">
//                                 Login
//                             </Button>
//                             <Button variant="outline" className="w-full">
//                                 Login with Google
//                             </Button>
//                         </form>
//                     </Form>
//                     <div className="mt-4 text-center text-sm">
//                         Don&apos;t have an account?{" "}
//                         <Link to="/register" className="underline">
//                             Sign up
//                         </Link>
//                     </div>
//                 </div>
//             </div>
//             <div className="bg-muted hidden md:block">
//                 <img
//                     src="https://source.unsplash.com/random/?finance,business"
//                     alt="Image"
//                     width="1920"
//                     height="1080"
//                     className="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
//                 />
//             </div>
//         </div>
//     )
// }

// export default LoginPage

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Shield, Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react'
import { toast } from '@/hooks/use-toast'

const LoginPage = () => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    })
    const [errors, setErrors] = useState({})
    const [isLoading, setIsLoading] = useState(false)

    const validateForm = () => {
        const newErrors = {}
        
        // Email validation
        if (!formData.email) {
            newErrors.email = 'Email is required'
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Invalid email format'
        }
        
        // Password validation
        if (!formData.password) {
            newErrors.password = 'Password is required'
        } else if (formData.password.length < 8) {
            newErrors.password = 'Password must be at least 8 characters'
        }
        
        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        
        if (!validateForm()) return
        
        setIsLoading(true)
        
        try {
            const response = await fetch(`${baseUrl}/api/auth/login`, {
                method: 'POST',
                headers: { "Content-type": "application/json" },
                credentials: 'include',
                body: JSON.stringify(formData)
            })
            const data = await response.json()
            
            if (data.status) {
                toast({
                    title: "Login Status!",
                    description: data.message,
                })
                navigate('/dashboard')
            } else {
                toast({
                    title: "Login Status!",
                    description: data.message,
                    variant: "destructive"
                })
            }
        } catch (error) {
            toast({
                title: "Login Status!",
                description: error.message,
                variant: "destructive"
            })
        } finally {
            setIsLoading(false)
        }
    }

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }))
        }
    }

    return (
        <div className="w-full grid grid-cols-1 lg:grid-cols-2 min-h-screen">
            {/* Left side - Form */}
            <div className="flex items-center justify-center py-12 px-4 bg-gradient-to-br from-slate-50 to-purple-50">
                <div className="mx-auto w-full max-w-md space-y-8">
                    {/* Header */}
                    <div className="text-center space-y-4">
                        <div className='flex justify-center'>
                            <div className='relative'>
                                <div className='absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full blur-lg opacity-50'></div>
                                <div className='relative bg-gradient-to-r from-purple-600 to-blue-600 p-3 rounded-full'>
                                    <Shield className='w-8 h-8 text-white' />
                                </div>
                            </div>
                        </div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                            Welcome Back
                        </h1>
                        <p className="text-gray-600">
                            Enter your credentials to access your account
                        </p>
                    </div>

                    {/* Form */}
                    <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
                        <div className="space-y-6">
                            {/* Email Field */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700">
                                    Email Address
                                </label>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                                    <Input 
                                        type="email"
                                        name="email"
                                        placeholder="you@example.com" 
                                        value={formData.email}
                                        onChange={handleChange}
                                        className="pl-10 h-12 border-gray-200 focus:border-purple-500 focus:ring-purple-500"
                                    />
                                </div>
                                {errors.email && (
                                    <p className="text-sm text-red-500">{errors.email}</p>
                                )}
                            </div>

                            {/* Password Field */}
                            <div className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <label className="text-sm font-medium text-gray-700">
                                        Password
                                    </label>
                                    {/* <Link
                                        to="/forgot-password"
                                        className="text-sm text-purple-600 hover:text-purple-700 font-medium"
                                    >
                                        Forgot password?
                                    </Link> */}
                                </div>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                                    <Input 
                                        type={showPassword ? "text" : "password"}
                                        name="password"
                                        value={formData.password}
                                        onChange={handleChange}
                                        className="pl-10 pr-10 h-12 border-gray-200 focus:border-purple-500 focus:ring-purple-500"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                                    >
                                        {showPassword ? (
                                            <EyeOff className="h-5 w-5" />
                                        ) : (
                                            <Eye className="h-5 w-5" />
                                        )}
                                    </button>
                                </div>
                                {errors.password && (
                                    <p className="text-sm text-red-500">{errors.password}</p>
                                )}
                            </div>

                            {/* Login Button */}
                            <Button 
                                onClick={handleSubmit}
                                disabled={isLoading}
                                className="w-full h-12 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-300"
                            >
                                <span className="flex items-center justify-center gap-2">
                                    {isLoading ? 'Signing In...' : 'Sign In'}
                                    {!isLoading && <ArrowRight className="h-4 w-4" />}
                                </span>
                            </Button>
                        </div>

                        {/* Sign up link */}
                        <div className="mt-6 text-center text-sm text-gray-600">
                            Don't have an account?{" "}
                            <Link to="/register" className="text-purple-600 hover:text-purple-700 font-semibold">
                                Create account
                            </Link>
                        </div>
                    </div>

                    {/* Security notice */}
                    <p className="text-center text-xs text-gray-500">
                        Protected by enterprise-grade encryption
                    </p>
                </div>
            </div>

            {/* Right side - Gradient Panel */}
            <div className="hidden lg:block relative bg-gradient-to-br from-purple-600 via-blue-600 to-purple-800 overflow-hidden">
                {/* Animated background elements */}
                <div className='absolute inset-0'>
                    <div className='absolute top-1/4 left-1/4 w-96 h-96 bg-white rounded-full mix-blend-overlay filter blur-3xl opacity-10 animate-pulse'></div>
                    <div className='absolute bottom-1/3 right-1/3 w-96 h-96 bg-purple-300 rounded-full mix-blend-overlay filter blur-3xl opacity-20 animate-pulse'></div>
                </div>
                
                {/* Content overlay */}
                <div className="relative h-full flex flex-col items-center justify-center p-12 text-white z-10">
                    <div className="max-w-md space-y-6 text-center">
                        <Shield className="w-20 h-20 mx-auto opacity-90" />
                        <h2 className="text-5xl font-bold">Secure and Intelligent Access</h2>
                        <p className="text-xl text-purple-100">
                        Your financial data is your most sensitive information. We protect it with the same level of security and privacy as a bank, so you can plan your future with complete peace of mind.
                        </p>
                        <div className="grid grid-cols-3 gap-4 pt-8">
                            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                                <p className="text-3xl font-bold">256-bit</p>
                                <p className="text-sm text-purple-100">Bank-Grade Encryption</p>
                            </div>
                            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                                <p className="text-3xl font-bold">99.9%</p>
                                <p className="text-sm text-purple-100">AI-Powered Insights</p>
                            </div>
                            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                                <p className="text-3xl font-bold">24/7</p>
                                <p className="text-sm text-purple-100">Data Privacy Guaranteed</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default LoginPage