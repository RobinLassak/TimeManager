using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public abstract class PersonBaseEntity : EntityBase
    {
        // Jmeno
        [Required, MaxLength(50)]
        public string FirstName { get; set; } = null!;


        // Prijmeni
        [Required, MaxLength(50)]
        public string LastName { get; set; } = null!;


        // Datum narozeni
        public DateTime? DateOfBirth { get; set; }

        
    }
}
