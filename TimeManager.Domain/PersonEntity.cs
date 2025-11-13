using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public class PersonEntity : EntityBase
    {
        // Jmeno
        [Required, MaxLength(50)]
        public string FirstName { get; set; } = null!;


        // Prijmeni
        [Required, MaxLength(50)]
        public string LastName { get; set; } = null!;


        // Datum narozeni
        public DateTime? DateOfBirth { get; set; }


        // Spolecnost
        public CompanyEntity? Company { get; set; }


        // Adresy
        public List<AdressEntity> Addresses { get; set; } = new();


        // Kontakty
        public List<ContactEntity> Contacts { get; set; } = new();


        // Bankovni ucty
        public List<BankAccountEntity> BankAccounts { get; set; } = new();


    }
}
