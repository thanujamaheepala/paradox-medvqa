import pic from "../logo.png";
const Header = ({ title }) => {
    return (
        <div className="text-center">
            <img src={pic} className="img-fluid " alt="Responsive image"/>
        </div>
    )
}

Header.defaultProps ={
    title : "Artificial Examiner"
}

export default Header
