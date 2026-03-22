import express from 'express'
import dotenv from 'dotenv'
import mongoose from 'mongoose'
import cookieParser from 'cookie-parser'
import AuthRoute from './routes/auth.route.js'
import cors from 'cors'
dotenv.config()
const app = express()


app.use(express.json())
app.use(cookieParser())
app.use(cors({
    origin: ['http://localhost:5173', 'http://localhost:3000'],
    credentials: true
}))

// Add middleware to ensure JSON responses
app.use((req, res, next) => {
    // Only set JSON content type for API routes
    if (req.originalUrl.startsWith('/api/')) {
        res.setHeader('Content-Type', 'application/json')
    }
    next()
})
const port = process.env.PORT
app.listen(port, () => {
    console.log('Our server is running on port:', port)
})


// database connection 

mongoose.connect(process.env.MONGODB_CONN).then(() => {
    console.log('Database connected')
}).catch(err => console.log('connection failed', err))


// router 

app.use('/api/auth', AuthRoute)

// Add a catch-all route for undefined API endpoints
app.use('/api/*', (req, res) => {
    res.status(404).json({
        status: false,
        message: `API endpoint ${req.originalUrl} not found`
    })
})

// Serve static files for any non-API routes (optional)
app.use(express.static('public'))

// Catch-all handler for non-API routes
app.get('*', (req, res) => {
    if (req.originalUrl.startsWith('/api/')) {
        res.status(404).json({
            status: false,
            message: `API endpoint ${req.originalUrl} not found`
        })
    } else {
        res.status(404).send('Page not found')
    }
})