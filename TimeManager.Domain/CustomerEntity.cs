using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TimeManager.Domain
{
    public class CustomerEntity : PersonBaseEntity
    {
        // Firma zakaznika
        public CompanyEntity? Company { get; set; }


        // Seznam kontaktu
        public List<ContactEntity> Contacts { get; set; } = new();


        // Seznam adres
        public List<AdressEntity> Addresses { get; set; } = new();
    }
}
