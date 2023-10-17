import Login from './components/UserLogin.vue'
import SignUp from './components/SignUp.vue'
import AdminLogin from './components/AdminLogin.vue'
import UserDash from './components/UserDash.vue'
import AdminDash from './components/AdminDash.vue'
import AddVenue from './components/AddVenue.vue'
import AddShow from'./components/AddShow.vue'
import EditVenue from './components/EditVenue.vue'
import EditShow from './components/EditShow.vue'
import Booking from './components/Booking.vue'
import AdminSignup from './components/AdminSignup.vue'
import ShowDash from './components/ShowDash.vue'
import PostedShows from './components/PostedShows.vue'
import BookingDashboard  from './components/BookDash.vue'
import SearchVenue from './components/SearchDash.vue'
import Summary from './components/Summary.vue'
import {createRouter, createWebHistory} from 'vue-router'

const routes=[
    {
        path : '/',
        redirect: '/Login',
    },
    {
        name:'Login',
        component: Login,
        path: '/Login'
    },
    {
        name:'SignUp',
        component: SignUp,
        path: '/sign-up'
    },
    {
        name:'AdminLogin',
        component: AdminLogin,
        path: '/admin-login'
    },
    {
        name:'UserDash',
        component: UserDash,
        path:'/userdash'
    },
    {
        name:'AdminDash',
        component: AdminDash,
        path:'/admindash'
    },
    {
        name:'AddVenue',
        component: AddVenue,
        path:'/addvenue'
    },
    {
        name:'AddShow',
        component: AddShow,
        path:'/addshow/:venue_id',
        props: true
    },
    {
        name:'EditVenue',
        component: EditVenue,
        path:'/editvenue/:venue_id',
        props: true
    },
    {
        name:'EditShow',
        component: EditShow,
        path:'/editshow/:venue_id/:show_id',
        props: true
    },
    {
        name:'Booking',
        component: Booking,
        path:'/booking/:venue_id/:show_id',
        props: true
    },
    {
        name:'AdminSignup',
        component: AdminSignup,
        path:'/adminsignup'
    },
    {
        name:'ShowDash',
        component: ShowDash,
        path:'/showdash/:venue_id',
        props: true
    },
    {
        name:'PostedShows',
        component: PostedShows,
        path:'/postedshows/:venue_id/shows',
        props: true
    },
    {
        name:'BookingDashboard',
        component: BookingDashboard,
        path:'/bookings',
    },
    {
        name:'SearchDash',
        component: SearchVenue,
        path:'/search',
    },
    {
        name:'Summary',
        component: Summary,
        path:'/summary',
    }


]


const router= createRouter({
    history: createWebHistory(),
    routes
})

export default router