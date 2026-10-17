import React from 'react';

const Card = ({ children, className }) => {
  return (
    <div 
      className={`rounded-lg border p-6 bg-white shadow-sm dark:bg-gray-800 ${className || ''}`}
    >
      {children}
    </div>
  );
};

Card.defaultProps = {
  className: ''
};

export default Card;