// import { Button } from '@/components/ui/button'
// import React from 'react'
// import { Link, useNavigate } from 'react-router-dom'
// import { zodResolver } from "@hookform/resolvers/zod"
// import { useForm } from "react-hook-form"
// import { z } from "zod"
// import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
// import { Input } from '@/components/ui/input'
// import { toast } from '@/hooks/use-toast'

// const RegisterPage = () => {

//     const baseUrl = import.meta.env.VITE_API_BASE_URL
//     const navigate = useNavigate()
//     const formSchema = z.object({
//         name: z.string().min(3, {
//             message: "Name must be at least 3 characters.",
//         }),
//         email: z.string().email(),
//         password: z.string().min(8, { message: "Password must be at least 8 characters." }),
//         confirm_password: z.string().min(8, { message: "Confirm password must be at least 8 characters." })
//     }).refine((data) => data.password === data.confirm_password, { message: 'Password and confirm password should be same.' })


//     const form = useForm({
//         resolver: zodResolver(formSchema),
//         defaultValues: {
//             name: '',
//             email: '',
//             password: '',
//             confirm_password: '',
//         },
//     })

//     const handleForm = async (values) => {
//         try {
//             const response = await fetch(`${baseUrl}/api/auth/register`, {
//                 method: 'Post',
//                 headers: { "Content-type": "application/json" },
//                 body: JSON.stringify(values)
//             })
//             const data = await response.json()
//             if (data.status) {
//                 toast({
//                     title: "Registration Status!",
//                     description: data.message,
//                 })
//                 navigate('/login')
//             } else {
//                 toast({
//                     title: "Registration Status!",
//                     description: data.message,
//                     variant: "destructive"
//                 })
//             }

//         } catch (error) {
//             toast({
//                 title: "Registration Status!",
//                 description: error.message,
//                 variant: "destructive"
//             })
//         }
//     }

//     return (
//         <div className="w-full grid grid-cols-1 lg:grid-cols-2 min-h-screen">
//             <div className="flex items-center justify-center py-12">
//                 <div className="mx-auto grid w-[350px] gap-6">
//                     <div className="grid gap-2 text-center">
//                         <h1 className="text-3xl font-bold">Register</h1>
//                         <p className="text-balance text-muted-foreground">
//                             Enter your information to create an account
//                         </p>
//                     </div>
//                     <Form {...form}>
//                         <form onSubmit={form.handleSubmit(handleForm)} className="grid gap-4">
//                             <div className="grid gap-2">
//                                 <FormField
//                                     control={form.control}
//                                     name="name"
//                                     render={({ field }) => (
//                                         <FormItem>
//                                             <FormLabel>Name</FormLabel>
//                                             <FormControl>
//                                                 <Input placeholder="Max Robinson" {...field} />
//                                             </FormControl>
//                                             <FormMessage />
//                                         </FormItem>
//                                     )}
//                                 />
//                             </div>
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
//                                             <FormLabel>Password</FormLabel>
//                                             <FormControl>
//                                                 <Input type="password" {...field} />
//                                             </FormControl>
//                                             <FormMessage />
//                                         </FormItem>
//                                     )}
//                                 />
//                             </div>
//                             <div className="grid gap-2">
//                                 <FormField
//                                     control={form.control}
//                                     name="confirm_password"
//                                     render={({ field }) => (
//                                         <FormItem>
//                                             <FormLabel>Confirm Password</FormLabel>
//                                             <FormControl>
//                                                 <Input type="password" {...field} />
//                                             </FormControl>
//                                             <FormMessage />
//                                         </FormItem>
//                                     )}
//                                 />
//                             </div>
//                             <Button type="submit" className="w-full">
//                                 Create an account
//                             </Button>
//                             <Button variant="outline" className="w-full">
//                                 Sign up with Google
//                             </Button>
//                         </form>
//                     </Form>
//                     <div className="mt-4 text-center text-sm">
//                         Already have an account?{" "}
//                         <Link to="/login" className="underline">
//                             Sign in
//                         </Link>
//                     </div>
//                 </div>
//             </div>
//             <div className="bg-muted">
//                 <img
//                     src="https://source.unsplash.com/random/?finance,business,money"
//                     alt="Image"
//                     width="1920"
//                     height="1080"
//                     className="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
//                 />
//             </div>
//         </div>
//     )
// }

// export default RegisterPage



// import { Button } from '@/components/ui/button' // import React from 'react' // import { Link, useNavigate } from 'react-router-dom' // import { zodResolver } from "@hookform/resolvers/zod" // import { useForm } from "react-hook-form" // import { z } from "zod" // import { Form, FormControl









import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { UserPlus, Mail, Lock, Eye, EyeOff, ArrowRight, User, CheckCircle } from 'lucide-react'
import { toast } from '@/hooks/use-toast'

const RegisterPage = () => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirm_password: ''
    })
    const [errors, setErrors] = useState({})
    const [isLoading, setIsLoading] = useState(false)

    // Password strength indicator
    const getPasswordStrength = (password) => {
        if (!password) return { strength: 0, text: '' }
        let strength = 0
        if (password.length >= 8) strength++
        if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++
        if (password.match(/[0-9]/)) strength++
        if (password.match(/[^a-zA-Z0-9]/)) strength++
        
        const strengthTexts = ['', 'Weak', 'Fair', 'Good', 'Strong']
        return { strength, text: strengthTexts[strength] }
    }

    const validateForm = () => {
        const newErrors = {}
        
        // Name validation
        if (!formData.name) {
            newErrors.name = 'Name is required'
        } else if (formData.name.length < 3) {
            newErrors.name = 'Name must be at least 3 characters'
        }
        
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
        
        // Confirm password validation
        if (!formData.confirm_password) {
            newErrors.confirm_password = 'Please confirm your password'
        } else if (formData.password !== formData.confirm_password) {
            newErrors.confirm_password = 'Passwords do not match'
        }
        
        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        
        if (!validateForm()) return
        
        setIsLoading(true)
        
        try {
            const response = await fetch(`${baseUrl}/api/auth/register`, {
                method: 'POST',
                headers: { "Content-type": "application/json" },
                body: JSON.stringify(formData)
            })
            const data = await response.json()
            
            if (data.status) {
                toast({
                    title: "Registration Status!",
                    description: data.message,
                })
                navigate('/login')
            } else {
                toast({
                    title: "Registration Status!",
                    description: data.message,
                    variant: "destructive"
                })
            }
        } catch (error) {
            toast({
                title: "Registration Status!",
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

    const passwordStrength = getPasswordStrength(formData.password)

    return (
        <div className="w-full grid grid-cols-1 lg:grid-cols-2 min-h-screen">
            {/* Left side - Form */}
            <div className="flex items-center justify-center py-12 px-4 bg-gradient-to-br from-slate-50 to-green-50">
                <div className="mx-auto w-full max-w-md space-y-8">
                    {/* Header */}
                    <div className="text-center space-y-4">
                        <div className='flex justify-center'>
                            <div className='relative'>
                                <div className='absolute inset-0 bg-gradient-to-r from-green-600 to-teal-600 rounded-full blur-lg opacity-50'></div>
                                <div className='relative bg-gradient-to-r from-green-600 to-teal-600 p-3 rounded-full'>
                                    <UserPlus className='w-8 h-8 text-white' />
                                </div>
                            </div>
                        </div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent">
                            Create Account
                        </h1>
                        <p className="text-gray-600">
                            Join us today and start your journey
                        </p>
                    </div>

                    {/* Form */}
                    <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
                        <div className="space-y-6">
                            {/* Name Field */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700">
                                    Full Name
                                </label>
                                <div className="relative">
                                    <User className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                                    <Input 
                                        type="text"
                                        name="name"
                                        placeholder="John Doe" 
                                        value={formData.name}
                                        onChange={handleChange}
                                        className="pl-10 h-12 border-gray-200 focus:border-green-500 focus:ring-green-500"
                                    />
                                </div>
                                {errors.name && (
                                    <p className="text-sm text-red-500">{errors.name}</p>
                                )}
                            </div>

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
                                        className="pl-10 h-12 border-gray-200 focus:border-green-500 focus:ring-green-500"
                                    />
                                </div>
                                {errors.email && (
                                    <p className="text-sm text-red-500">{errors.email}</p>
                                )}
                            </div>

                            {/* Password Field */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700">
                                    Password
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                                    <Input 
                                        type={showPassword ? "text" : "password"}
                                        name="password"
                                        value={formData.password}
                                        onChange={handleChange}
                                        className="pl-10 pr-10 h-12 border-gray-200 focus:border-green-500 focus:ring-green-500"
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
                                
                                {/* Password strength indicator */}
                                {formData.password && (
                                    <div className="space-y-1">
                                        <div className="flex gap-1">
                                            {[1, 2, 3, 4].map((level) => (
                                                <div
                                                    key={level}
                                                    className={`h-1 flex-1 rounded-full transition-colors ${
                                                        level <= passwordStrength.strength
                                                            ? level <= 2
                                                                ? 'bg-orange-500'
                                                                : 'bg-green-500'
                                                            : 'bg-gray-200'
                                                    }`}
                                                />
                                            ))}
                                        </div>
                                        {passwordStrength.text && (
                                            <p className={`text-xs ${
                                                passwordStrength.strength <= 2 
                                                    ? 'text-orange-500' 
                                                    : 'text-green-500'
                                            }`}>
                                                Password strength: {passwordStrength.text}
                                            </p>
                                        )}
                                    </div>
                                )}
                            </div>

                            {/* Confirm Password Field */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700">
                                    Confirm Password
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                                    <Input 
                                        type={showConfirmPassword ? "text" : "password"}
                                        name="confirm_password"
                                        value={formData.confirm_password}
                                        onChange={handleChange}
                                        className="pl-10 pr-10 h-12 border-gray-200 focus:border-green-500 focus:ring-green-500"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                        className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                                    >
                                        {showConfirmPassword ? (
                                            <EyeOff className="h-5 w-5" />
                                        ) : (
                                            <Eye className="h-5 w-5" />
                                        )}
                                    </button>
                                </div>
                                {errors.confirm_password && (
                                    <p className="text-sm text-red-500">{errors.confirm_password}</p>
                                )}
                                {formData.confirm_password && formData.password === formData.confirm_password && (
                                    <p className="text-sm text-green-500 flex items-center gap-1">
                                        <CheckCircle className="h-4 w-4" />
                                        Passwords match
                                    </p>
                                )}
                            </div>

                            {/* Register Button */}
                            <Button 
                                onClick={handleSubmit}
                                disabled={isLoading}
                                className="w-full h-12 bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-300"
                            >
                                <span className="flex items-center justify-center gap-2">
                                    {isLoading ? 'Creating Account...' : 'Create Account'}
                                    {!isLoading && <ArrowRight className="h-4 w-4" />}
                                </span>
                            </Button>
                        </div>

                        {/* Sign in link */}
                        <div className="mt-6 text-center text-sm text-gray-600">
                            Already have an account?{" "}
                            <Link to="/login" className="text-green-600 hover:text-green-700 font-semibold">
                                Sign in
                            </Link>
                        </div>
                    </div>

                    {/* Terms notice */}
                    <p className="text-center text-xs text-gray-500">
                        By creating an account, you agree to our Terms of Service and Privacy Policy
                    </p>
                </div>
            </div>

            {/* Right side - Gradient Panel */}
            <div className="hidden lg:block relative bg-gradient-to-br from-green-600 via-teal-600 to-green-800 overflow-hidden">
                {/* Animated background elements */}
                <div className='absolute inset-0'>
                    <div className='absolute top-1/4 left-1/4 w-96 h-96 bg-white rounded-full mix-blend-overlay filter blur-3xl opacity-10 animate-pulse'></div>
                    <div className='absolute bottom-1/3 right-1/3 w-96 h-96 bg-teal-300 rounded-full mix-blend-overlay filter blur-3xl opacity-20 animate-pulse'></div>
                </div>
                
                {/* Content overlay */}
                <div className="relative h-full flex flex-col items-center justify-center p-12 text-white z-10">
                    <div className="max-w-md space-y-6 text-center">
                        <UserPlus className="w-20 h-20 mx-auto opacity-90" />
                        <h2 className="text-5xl font-bold">Join Our Community
</h2>
                        <p className="text-xl text-green-100">
                        Build Your Financial Future, Intelligently.
                        </p>
                        
                        {/* Benefits list */}
                        <div className="space-y-4 pt-8 text-left">
                            <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm rounded-lg p-4">
                                <CheckCircle className="h-6 w-6 text-green-300 flex-shrink-0" />
                                <p className="text-green-50">Build Your Financial Future, Intelligently.</p>
                            </div>
                            <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm rounded-lg p-4">
                                <CheckCircle className="h-6 w-6 text-green-300 flex-shrink-0" />
                                <p className="text-green-50">Unbiased Insurance Analysis</p>
                            </div>
                            <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm rounded-lg p-4">
                                <CheckCircle className="h-6 w-6 text-green-300 flex-shrink-0" />
                                <p className="text-green-50">Personalized Investment & Affordability Roadmaps</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default RegisterPage
