using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    // Typy kontaktu
    public enum ContactType
    {
        Personal,
        Business,
        Other
    }

    // Zpusoby komunikace
    public enum CommunicationType
    {
        Email,
        Phone,
    }
    public class ContactEntity : EntityBase
    {
        // Zpusob komunikace
        [Required]
        public CommunicationType Communication { get; set; }


        // Typ komunikace
        [Required]
        public ContactType Type { get; set; }

        // Hodnota kontaktu (email, telefonni cislo, atd.)
        [Required, MaxLength(100)]
        public string Value { get; set; } = null!;

        // Popis kontaktu
        [MaxLength(500)]
        public string? Description { get; set; }

    }
}
